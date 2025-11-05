# demo_hash.py
from src.extensible_hash.hash_extensible import ExtensibleHash

def demo_insert(h: ExtensibleHash):
    print("\n=== INSERÇÕES ===")
    for k in [1, 2, 3, 4, 5, 6, 7]:
        print(f"\nInserindo chave {k}...")
        h.insert(k, f"valor_{k}")
        h.display()
    print("\n-- Inserções concluídas --\n")


def demo_search(h: ExtensibleHash):
    print("\n=== BUSCAS ===")
    for k in [1, 4, 6, 10]:
        v = h.search(k)
        if v is not None:
            print(f"Chave {k} encontrada → {v}")
        else:
            print(f"Chave {k} não encontrada!")
    print("\n-- Buscas concluídas --\n")


def demo_remove(h: ExtensibleHash):
    print("\n=== REMOÇÕES ===")
    for k in [2, 5, 10]:
        result = h.remove(k)
        msg = "Removido" if result else "Não encontrado"
        print(f"Chave {k}: {msg}")
        h.display()
    print("\n-- Remoções concluídas --\n")


if __name__ == "__main__":
    print("==== Demonstração da Tabela Hash Extensível ====")
    h = ExtensibleHash(bucket_size=2)

    demo_insert(h)
    demo_search(h)
    demo_remove(h)

    print(" Demonstração finalizada ")
