from src.bplustree.bptree import BPlusTree, LeafNode, InternalNode

def print_leaves(tree):
    n = tree.root
    while isinstance(n, InternalNode):
        n = n.children[0]
    parts = []
    while n:
        parts.append(str(n.keys))
        n = n.next_leaf
    print("Folhas:", " -> ".join(parts))

def main():
    t = BPlusTree(order=4)
    for k in [10,20,5,6,12,30,7,17,3,25,15,16,18]:
        t.insert(k, f"v{k}")
    print("17 ->", t.search(17))
    print("999 ->", t.search(999))
    print("remove 20:", t.remove(20))
    print("remove 12:", t.remove(12))
    print_leaves(t)

if __name__ == "__main__":
    main()
