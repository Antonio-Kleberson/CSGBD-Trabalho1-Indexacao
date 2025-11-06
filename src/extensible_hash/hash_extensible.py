# src/extensible_hash/hash_extensible.py
from typing import Any, List, Tuple


class Bucket:
    """Representa um bucket da tabela hash extensível."""

    def __init__(self, capacity: int, local_depth: int):
        self.capacity = capacity
        self.local_depth = local_depth
        self.items: List[Tuple[int, Any]] = []

    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    def insert(self, key: int, value: Any):
        for i, (k, _) in enumerate(self.items):
            if k == key:  # atualização
                self.items[i] = (key, value)
                return
        self.items.append((key, value))

    def search(self, key: int):
        for k, v in self.items:
            if k == key:
                return v
        return None

    def remove(self, key: int) -> bool:
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                return True
        return False

    def __repr__(self):
        return f"Bucket(ld={self.local_depth}, items={self.items})"


class ExtensibleHash:
    """
    Implementação completa do Hash Extensível com splits e duplicação de diretório.
    """

    def __init__(self, bucket_size: int):
        self.bucket_size = bucket_size
        self.global_depth = 1
        b = Bucket(capacity=bucket_size, local_depth=1)
        self.directory = [b, b]

    # ===== Funções auxiliares =====
    def _hash(self, key: int) -> int:
        """Usa bits menos significativos da chave."""
        mask = (1 << self.global_depth) - 1
        return key & mask

    def _double_directory(self):
        """Dobra o diretório e aumenta profundidade global."""
        self.directory += self.directory[:]  # duplica lista
        self.global_depth += 1

 
    def _possible_shrink(self):
        """
        Tenta reduzir (enxugar) a profundidade global enquanto possível.
        Condição simples usada aqui: se nenhum bucket tem local_depth == global_depth,
        então podemos cortar o diretório ao meio e decrementar global_depth.
        Repetimos até não ser possível.
        """
        while self.global_depth > 1:
            # se existe bucket com local_depth == global_depth -> não encolher
            any_eq = any(b.local_depth == self.global_depth for b in set(self.directory))
            if any_eq:
                break
            # Enxugar: manter a metade inicial do diretório
            half = len(self.directory) // 2
            self.directory = self.directory[:half]
            self.global_depth -= 1

    def _split_bucket(self, idx: int):
        """Divide um bucket cheio e redistribui suas chaves."""
        old_bucket = self.directory[idx]
        old_depth = old_bucket.local_depth

        # Se o bucket já está na profundidade global, duplicar o diretório
        if old_depth == self.global_depth:
            self._double_directory()

        # Novo bucket com profundidade local +1
        new_depth = old_depth + 1
        old_bucket.local_depth = new_depth
        new_bucket = Bucket(capacity=self.bucket_size, local_depth=new_depth)

        # Atualizar ponteiros do diretório
        for i in range(len(self.directory)):
            if self.directory[i] is old_bucket:
                bit = (i >> (new_depth - 1)) & 1
                if bit == 1:
                    self.directory[i] = new_bucket

        # Redistribuir itens entre os dois buckets
        all_items = old_bucket.items[:]
        old_bucket.items.clear()
        for k, v in all_items:
            new_idx = self._hash(k)
            self.directory[new_idx].insert(k, v)

    # ===== Operações principais =====
    def insert(self, key: int, value: Any):
        idx = self._hash(key)
        bucket = self.directory[idx]

        if not bucket.is_full():
            bucket.insert(key, value)
            return

        # Se estiver cheio, faz split e tenta de novo
        self._split_bucket(idx)
        self.insert(key, value)

    def search(self, key: int):
        idx = self._hash(key)
        return self.directory[idx].search(key)

    def remove(self, key: int) -> bool:
        """
        Remove uma chave; após remoção tenta fazer merges com bucket 'buddy'
        e reduzir a profundidade global quando aplicável.
        """
        idx = self._hash(key)
        bucket = self.directory[idx]
        removed = bucket.remove(key)
        if not removed:
            return False

        # Após remover, tentar merges iterativos enquanto possível
        self._try_merge(idx)
        # Tentar reduzir a profundidade global se possível
        self._possible_shrink()
        return True

    # ---------------- merge helpers ----------------
    def _get_bucket_indices(self, bucket):
        """Retorna todos os índices do diretório que apontam para 'bucket'."""
        return [i for i, b in enumerate(self.directory) if b is bucket]

    def _try_merge(self, any_index: int):
        """
        Tenta merge recursivo a partir do bucket que contém any_index.
        Regras (padrão simples):
        - Para o bucket com local_depth d, seu 'par' (buddy) é o índice com bit (d-1) flipado.
        - Só fazemos merge se o buddy existir, tiver mesma local_depth e a soma das chaves couber em um bucket.
        - Após merge, decrementa local_depth do bucket resultante e atualiza ponteiros do diretório.
        - Repetimos para o bucket resultante (pode encadear).
        """
        bucket = self.directory[any_index]
        while True:
            d = bucket.local_depth
            # se d == 1 não tem como fazer merge (pelo menos parar condição)
            if d <= 1:
                break

            # escolha um índice representativo que aponte para este bucket
            indices = self._get_bucket_indices(bucket)
            if not indices:
                break
            rep_idx = indices[0]

            # calcula buddy index (flip do bit d-1)
            buddy_idx = rep_idx ^ (1 << (d - 1))
            buddy_bucket = self.directory[buddy_idx]

            # só merge se buddy diferente, mesma profundidade local e capacidade combinada ok
            if buddy_bucket is bucket or buddy_bucket.local_depth != d:
                break

            combined_size = len(bucket.items) + len(buddy_bucket.items)
            if combined_size > self.bucket_size:
                break  # não cabe combinado

            # Fazer merge: vamos escolher buddy_bucket como recipiente (arbitrário)
            recipient = buddy_bucket
            donor = bucket

            # mover itens do donor para recipient
            recipient.items.extend(donor.items)
            donor.items.clear()

            # reduzir local_depth do recipient
            recipient.local_depth = d - 1

            # atualizar todas as entradas do diretório que apontavam para donor ou recipient:
            # para cada i que tinha pointer para donor ou recipient e cujo prefix de (d-1) bits seja igual
            # ao prefix base, apontar para recipient
            # implementação prática: para todo i, se seu bit-prefix até d-1 combinar com o bucket base, set pointer
            for i in range(len(self.directory)):
                # se índice i corresponde ao grupo que apontava para donor ou recipient antes,
                # reatribuir para recipient quando o prefix de d-1 bits for igual
                mask = (1 << (d - 1)) - 1
                # prefix sem o bit de ordenação de d-1
                if (i >> (d - 1)) == (rep_idx >> (d - 1)):
                    # isto garante que as entradas daquele grupo agora apontem para recipient
                    if self.directory[i] is donor or self.directory[i] is recipient:
                        self.directory[i] = recipient

            # agora o bucket merged é 'recipient'; continue tentando merge para profundidade menor
            bucket = recipient

    # ===== Exibição =====
    def display(self):
        print(f"\n===== Estado Atual da Tabela Hash =====")
        print(f"Profundidade Global: {self.global_depth}")
        seen = {}
        for i, b in enumerate(self.directory):
            if id(b) not in seen:
                seen[id(b)] = f"B{len(seen)}"
            label = seen[id(b)]
            print(f"{i:0{self.global_depth}b} → {label} {b}")
        print("=======================================\n")
