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
        idx = self._hash(key)
        return self.directory[idx].remove(key)

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
