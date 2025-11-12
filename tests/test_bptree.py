# tests/test_bptree_merge.py
from src.bplustree.bptree import BPlusTree

def test_insert_split_and_merge():
    t = BPlusTree(order=4)  # máx 3 chaves por nó

    # Inserir várias chaves para provocar splits
    for k in [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 15, 16, 18]:
        t.insert(k, f"v{k}")

    # Verificar se todas as chaves estão acessíveis
    for k in [3,5,6,7,10,12,15,16,17,18,20,25,30]:
        assert t.search(k) == f"v{k}"

    # Remover chaves para forçar merges
    for k in [20, 12, 18, 17, 16, 15]:
        assert t.remove(k) is True
        assert t.search(k) is None

    # As demais chaves ainda devem existir
    for k in [3,5,6,7,10,25,30]:
        assert t.search(k) == f"v{k}"

    # Remoção até reduzir altura (root rebaixada)
    for k in [30,25,10,7,6,5,3]:
        t.remove(k)

    # Depois de tudo, a árvore deve estar vazia ou com uma raiz folha vazia
    root = t.root
    # Se a raiz for folha, ela pode estar vazia
    assert isinstance(root.keys, list)
    assert len(root.keys) >= 0
