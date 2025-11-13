from src.bplustree.bptree import BPlusTree, LeafNode, InternalNode

# Percorre a árvore B+ até encontrar o primeiro nó folha e imprime todas as folhas.
def print_leaves(tree):
    n = tree.root # Desce até a primeira folha
    while isinstance(n, InternalNode):
        n = n.children[0]
    parts = []
    while n:  # Percorre as folhas encadeadas utilizando next_leaf
        parts.append(str(n.keys))
        n = n.next_leaf
    print("Folhas:", " -> ".join(parts))

def main():
    t = BPlusTree(order=4)
    for k in [10,20,5,6,12,30,7,17,3,25,15,16,18]:
        t.insert(k, f"v{k}")
    # Busca por uma chave existente e uma inexistente
    print("17 ->", t.search(17))
    print("999 ->", t.search(999))
    # Remove duas chaves
    print("remove 20:", t.remove(20))
    print("remove 12:", t.remove(12))
    print_leaves(t)

if __name__ == "__main__":
    main()
