# src/extensible_hash/hash_extensible.py
from typing import Any, List, Tuple


class Bucket:
    """
    Representa um bucket (balde) da Tabela Hash Extensível.
    Cada bucket tem:
    - capacidade máxima (bucket_size)
    - profundidade local (local_depth)
    - lista de pares (chave, valor)
    """

    def __init__(self, capacity: int, local_depth: int):
        self.capacity = capacity
        self.local_depth = local_depth
        self.items: List[Tuple[int, Any]] = []

    def is_full(self) -> bool:
        """Retorna True se o bucket atingiu sua capacidade máxima."""
        return len(self.items) >= self.capacity

    def insert(self, key: int, value: Any):
        """Insere ou atualiza um par (chave, valor) dentro do bucket."""
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items[i] = (key, value)
                return
        self.items.append((key, value))
        self.items.sort(key=lambda x: x[0])  # mantém ordenado por chave

    def search(self, key: int):
        """Busca o valor associado à chave neste bucket."""
        for k, v in self.items:
            if k == key:
                return v
        return None

    def remove(self, key: int) -> bool:
        """Remove uma chave do bucket, se existir."""
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                return True
        return False

    def __repr__(self):
        return f"Bucket(ld={self.local_depth}, items={self.items})"


class ExtensibleHash:
    """
    Implementação da Tabela Hash Extensível.
    - global_depth: número de bits considerados da função hash.
    - directory: lista de ponteiros para buckets.
    """

    def __init__(self, bucket_size: int):
        self.bucket_size = bucket_size
        self.global_depth = 1
        # Diretório começa com 2 entradas, apontando para o mesmo bucket
        b = Bucket(capacity=bucket_size, local_depth=1)
        self.directory = [b, b]

    def _hash(self, key: int) -> int:
        """Função de hashing simples (usa bits menos significativos)."""
        mask = (1 << self.global_depth) - 1
        return key & mask

    def _double_directory(self):
        """Dobra o tamanho do diretório e incrementa a profundidade global."""
        self.directory = self.directory + self.directory[:]
        self.global_depth += 1

    def _split_bucket(self, idx: int):
        """Divide um bucket cheio e redistribui suas chaves."""
        bucket = self.directory[idx]

        # Se a profundidade local for igual à global, duplicar diretório
        if bucket.local_depth == self.global_depth:
            self._double_directory()

        # Cria novo bucket e atualiza profundidade local
        new_depth = bucket.local_depth + 1
        bucket.local_depth = new_depth
        new_bucket = Bucket(capacity=self.bucket_size, local_depth=new_depth)

        # Atualiza diretório para apontar corretamente
        for i, ptr in enumerate(self.directory):
            if ptr is bucket:
                bit = (i >> (new_depth - 1)) & 1
                if bit == 1:
                    self.directory[i] = new_bucket

        # Redistribui os itens do bucket antigo
        all_items = bucket.items[:]
        bucket.items.clear()
        for k, v in all_items:
            self.insert(k, v)

    def insert(self, key: int, value: Any):
        """Insere um novo par (chave, valor) na estrutura."""
        idx = self._hash(key)
        bucket = self.directory[idx]

        if not bucket.is_full():
            bucket.insert(key, value)
            return

        # Caso o bucket esteja cheio, precisamos dividi-lo
        self._split_bucket(idx)
        # Reinsere após o split (agora haverá espaço)
        self.insert(key, value)

    def search(self, key: int):
        """Busca um valor pela chave."""
        idx = self._hash(key)
        return self.directory[idx].search(key)

    def remove(self, key: int) -> bool:
        """Remove um registro (sem merge nesta fase)."""
        idx = self._hash(key)
        return self.directory[idx].remove(key)

    def display(self):
        """Exibe o diretório e os buckets."""
        print(f"Global depth: {self.global_depth}")
        seen = {}
        for i, b in enumerate(self.directory):
            if id(b) not in seen:
                seen[id(b)] = f"B{len(seen)}"
            print(f"{i:0{self.global_depth}b} → {seen[id(b)]} {b}")
