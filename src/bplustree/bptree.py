import math

class Node:
    def __init__(self, order: int):
        self.order = order
        self.keys = []
        self.parent = None

    def is_full(self):
        return len(self.keys) > self.order - 1

    def find_index(self, key):
        for i, k in enumerate(self.keys):
            if key < k:
                return i
        return len(self.keys)


class LeafNode(Node):
    def __init__(self, order: int):
        super().__init__(order)
        self.values = []
        self.next_leaf = None

    def add_key_value(self, key, value):
        index = self.find_index(key)
        if index < len(self.keys) and self.keys[index] == key:
            self.values[index] = value
            return
        self.keys.insert(index, key)
        self.values.insert(index, value)

    def split(self):
        mid = math.ceil(len(self.keys) / 2)
        new_leaf = LeafNode(self.order)
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf
        key_promoted = new_leaf.keys[0]
        return key_promoted, new_leaf


class InternalNode(Node):
    def __init__(self, order: int):
        super().__init__(order)
        self.children = []

    def add_key_child(self, key, child_node):
        index = self.find_index(key)
        self.keys.insert(index, key)
        self.children.insert(index + 1, child_node)
        child_node.parent = self

    def split(self):
        mid = len(self.keys) // 2
        key_promoted = self.keys[mid]
        new_node = InternalNode(self.order)
        new_node.keys = self.keys[mid + 1:]
        new_node.children = self.children[mid + 1:]
        self.keys = self.keys[:mid]
        self.children = self.children[:mid + 1]
        for child in new_node.children:
            child.parent = new_node
        return key_promoted, new_node


class BPlusTree:
    def __init__(self, order: int):
        if order < 3:
            raise ValueError("A ordem da Árvore B+ deve ser no mínimo 3.")
        self.order = order
        self.root = LeafNode(order)

    def _find_leaf(self, key) -> LeafNode:
        node = self.root
        while not isinstance(node, LeafNode):
            index = node.find_index(key)
            node = node.children[index]
        return node

    def insert(self, key: int, value: any):
        leaf = self._find_leaf(key)
        leaf.add_key_value(key, value)
        if leaf.is_full():
            key_promoted, new_node = leaf.split()
            self._handle_split(leaf, key_promoted, new_node)

    def _handle_split(self, old_node: Node, key_promoted: int, new_node: Node):
        if old_node.parent is None:
            new_root = InternalNode(self.order)
            new_root.keys = [key_promoted]
            new_root.children = [old_node, new_node]
            old_node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
            return
        parent = old_node.parent
        parent.add_key_child(key_promoted, new_node)
        if parent.is_full():
            key_parent_promoted, new_parent = parent.split()
            self._handle_split(parent, key_parent_promoted, new_parent)

    def search(self, key: int) -> any:
        leaf = self._find_leaf(key)
        try:
            index = leaf.keys.index(key)
            return leaf.values[index]
        except ValueError:
            return None

    def remove(self, key: int) -> bool:
        leaf = self._find_leaf(key)
        try:
            idx = leaf.keys.index(key)
        except ValueError:
            return False
        leaf.keys.pop(idx)
        leaf.values.pop(idx)
        if leaf is self.root:
            return True
        self._rebalance_after_delete(leaf)
        return True

    def _leaf_min_keys(self) -> int:
        return math.ceil((self.order - 1) / 2)

    def _internal_min_keys(self) -> int:
        return math.ceil(self.order / 2) - 1

    def _get_siblings(self, node):
        parent = node.parent
        assert parent is not None
        idx = parent.children.index(node)
        left_sib = parent.children[idx - 1] if idx - 1 >= 0 else None
        right_sib = parent.children[idx + 1] if idx + 1 < len(parent.children) else None
        return parent, idx, left_sib, right_sib

    def _rebalance_after_delete(self, node):
        if node is self.root:
            if isinstance(node, InternalNode) and len(node.keys) == 0:
                child = node.children[0]
                child.parent = None
                self.root = child
            return
        if isinstance(node, LeafNode):
            self._fix_leaf_underflow(node)
        else:
            self._fix_internal_underflow(node)

    def _fix_leaf_underflow(self, leaf: 'LeafNode'):
        min_keys = self._leaf_min_keys()
        if len(leaf.keys) >= min_keys:
            return
        parent, idx, left_sib, right_sib = self._get_siblings(leaf)
        if isinstance(left_sib, LeafNode) and len(left_sib.keys) > min_keys:
            k = left_sib.keys.pop()
            v = left_sib.values.pop()
            leaf.keys.insert(0, k)
            leaf.values.insert(0, v)
            parent.keys[idx - 1] = leaf.keys[0]
            return
        if isinstance(right_sib, LeafNode) and len(right_sib.keys) > min_keys:
            k = right_sib.keys.pop(0)
            v = right_sib.values.pop(0)
            leaf.keys.append(k)
            leaf.values.append(v)
            parent.keys[idx] = right_sib.keys[0]
            return
        if isinstance(left_sib, LeafNode):
            left_sib.keys.extend(leaf.keys)
            left_sib.values.extend(leaf.values)
            left_sib.next_leaf = leaf.next_leaf
            del parent.keys[idx - 1]
            del parent.children[idx]
            self._rebalance_after_delete(parent)
        elif isinstance(right_sib, LeafNode):
            leaf.keys.extend(right_sib.keys)
            leaf.values.extend(right_sib.values)
            leaf.next_leaf = right_sib.next_leaf
            del parent.keys[idx]
            del parent.children[idx + 1]
            self._rebalance_after_delete(parent)

    def _fix_internal_underflow(self, node: 'InternalNode'):
        min_keys = self._internal_min_keys()
        if len(node.keys) >= min_keys:
            return
        parent, idx, left_sib, right_sib = self._get_siblings(node)
        if isinstance(left_sib, InternalNode) and len(left_sib.keys) > min_keys:
            sep = parent.keys[idx - 1]
            borrow_key = left_sib.keys.pop()
            borrow_child = left_sib.children.pop()
            node.keys.insert(0, sep)
            node.children.insert(0, borrow_child)
            borrow_child.parent = node
            parent.keys[idx - 1] = borrow_key
            return
        if isinstance(right_sib, InternalNode) and len(right_sib.keys) > min_keys:
            sep = parent.keys[idx]
            borrow_key = right_sib.keys.pop(0)
            borrow_child = right_sib.children.pop(0)
            node.keys.append(sep)
            node.children.append(borrow_child)
            borrow_child.parent = node
            parent.keys[idx] = borrow_key
            return
        if isinstance(left_sib, InternalNode):
            sep = parent.keys[idx - 1]
            left_sib.keys.append(sep)
            left_sib.keys.extend(node.keys)
            left_sib.children.extend(node.children)
            for ch in node.children:
                ch.parent = left_sib
            del parent.keys[idx - 1]
            del parent.children[idx]
            self._rebalance_after_delete(parent)
        elif isinstance(right_sib, InternalNode):
            sep = parent.keys[idx]
            node.keys.append(sep)
            node.keys.extend(right_sib.keys)
            node.children.extend(right_sib.children)
            for ch in right_sib.children:
                ch.parent = node
            del parent.keys[idx]
            del parent.children[idx + 1]
            self._rebalance_after_delete(parent)
            
    def display(self):
        """Exibe a estrutura da Árvore B+ de forma hierárquica."""
        print(f"\n===== Estrutura da Árvore B+ (Ordem {self.order}) =====")

        if not self.root:
            print("(Árvore vazia)")
            return

        queue = [(self.root, 0)]
        current_level = 0
        level_nodes = []

        while queue:
            node, level = queue.pop(0)
            if level != current_level:
                print(f"Nível {current_level}: ", end="")
                print(" | ".join(level_nodes))
                level_nodes = []
                current_level = level

            tipo = "F" if isinstance(node, LeafNode) else "I"
            level_nodes.append(f"{tipo}{node.keys}")

            if isinstance(node, InternalNode):
                for child in node.children:
                    queue.append((child, level + 1))

        print(f"Nível {current_level}: ", end="")
        print(" | ".join(level_nodes))
        print("=======================================================")
