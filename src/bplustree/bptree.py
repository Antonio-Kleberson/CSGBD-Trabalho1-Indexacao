import math
import os
from graphviz import Digraph

# É a base de todos os nós da Árvore B+.
# Ela guarda as chaves, o ponteiro para o pai, e sabe qual a capacidade máxima do nó.
class Node:
    def __init__(self, order: int):
        # Ordem da árvore (máx. de chaves por nó = order - 1)
        self.order = order
        self.keys = []
        self.parent = None

    def is_full(self):
        # Retorna True se o nó excedeu o limite de chaves
        return len(self.keys) > self.order - 1

    def find_index(self, key):
        # Encontra a posição correta onde a chave deve ser inserida
        for i, k in enumerate(self.keys):
            if key < k:
                return i
        return len(self.keys)

# Representa os nós folhas da Árvore B+.
class LeafNode(Node):
    """As folhas são encadeadas utilizando next_leaf, e
        permite percorrer todas as entradas da árvore em ordem crescente."""
    def __init__(self, order: int):
        super().__init__(order)
        self.values = []
        # Ponteiro para a próxima folha (lista encadeada das folhas)
        self.next_leaf = None

    """insere chave e valor na posição correta, mantendo a folha ordenada."""
    def add_key_value(self, key, value):
        # Encontra a posição correta da chave dentro da folha
        index = self.find_index(key)

        # Se a chave já existe, atualiza o valor
        if index < len(self.keys) and self.keys[index] == key:
            self.values[index] = value
            return

        # Insere chave e valor mantendo ordem
        self.keys.insert(index, key)
        self.values.insert(index, value)

    """divide a folha ao meio, ajusta o encadeamento e devolve a
        chave que deve subir para o nó pai."""
    def split(self):
        # Calcula ponto de corte para dividir a folha
        mid = math.ceil(len(self.keys) / 2)

        # Cria nova folha com a metade direita das chaves/valores
        new_leaf = LeafNode(self.order)
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]

        # Mantém metade esquerda nesta folha
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]

        # Ajusta o encadeamento entre folhas
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf

        # A chave promovida é a menor da nova folha
        key_promoted = new_leaf.keys[0]
        return key_promoted, new_leaf


class InternalNode(Node):
    """Representa os nós internos da Árvore B+."""
    def __init__(self, order: int):
        super().__init__(order)
        # Lista de ponteiros para os filhos deste nó
        self.children = []

    """Ao receber uma chave promovida de um split, esse metodo insere tanto
        a chave quanto o ponteiro do filho correspondente na posição correta."""
    def add_key_child(self, key, child_node):
        # Encontra a posição de inserção com base na chave
        index = self.find_index(key)

        # Insere a chave no lugar certo
        self.keys.insert(index, key)

        # Insere o filho correspondente à direita da chave
        self.children.insert(index + 1, child_node)
        child_node.parent = self  # Atualiza o pai do filho

    """divide o nó interno ao meio e devolve a chave que deve subir para o pai."""
    def split(self):
        # Índice da chave mediana que será promovida para o pai
        mid = len(self.keys) // 2
        key_promoted = self.keys[mid]

        # Novo nó interno que receberá a metade direita
        new_node = InternalNode(self.order)
        new_node.keys = self.keys[mid + 1:]
        new_node.children = self.children[mid + 1:]

        # Este nó mantém a metade esquerda
        self.keys = self.keys[:mid]
        self.children = self.children[:mid + 1]

        # Atualiza o pai dos filhos movidos para o novo nó
        for child in new_node.children:
            child.parent = new_node

        # Retorna a chave promovida e o novo nó criado
        return key_promoted, new_node


"""Implementa uma Árvore B+ com operações de inserção, busca e remoção."""
class BPlusTree:
    def __init__(self, order: int):
        """Cria a árvore com a ordem informada e inicializa a raiz como uma folha."""
        if order < 3:
            raise ValueError("A ordem da Árvore B+ deve ser no mínimo 3.")
        self.order = order
        self.root = LeafNode(order)

    """Percorre a árvore até encontrar a folha onde a chave deve estar."""
    def _find_leaf(self, key) -> LeafNode:
        node = self.root
        while not isinstance(node, LeafNode):
            index = node.find_index(key)
            node = node.children[index]
        return node

    """Insere uma nova chave e valor na árvore, realizando splits conforme necessário."""
    def insert(self, key: int, value: any):
        leaf = self._find_leaf(key)
        leaf.add_key_value(key, value)
        if leaf.is_full():
            key_promoted, new_node = leaf.split()
            self._handle_split(leaf, key_promoted, new_node)
        # Gera imagem após a inserção (com snapshot automático, se habilitado)
        self._snapshot(f"ins_{key}")

    """Propaga o split para o pai; se não houver pai, cria uma nova raiz."""
    def _handle_split(self, old_node: Node, key_promoted: int, new_node: Node):
        # Caso especial: o nó que estourou era a raiz
        if old_node.parent is None:
            new_root = InternalNode(self.order)
            new_root.keys = [key_promoted]
            new_root.children = [old_node, new_node]
            old_node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
            return

        parent = old_node.parent

        # Caso geral: insere a chave promovida no pai existente
        pos = parent.children.index(old_node)
        parent.keys.insert(pos, key_promoted)
        parent.children.insert(pos + 1, new_node)
        new_node.parent = parent

        # Se o pai também encher, faz split recursivamente
        if len(parent.keys) > parent.order - 1:
            key_parent_promoted, new_parent = parent.split()
            self._handle_split(parent, key_parent_promoted, new_parent)

    """Busca a chave na folha correspondente e retorna o valor (ou None se não existir)."""
    def search(self, key: int) -> any:
        leaf = self._find_leaf(key)
        try:
            index = leaf.keys.index(key)
            return leaf.values[index]
        except ValueError:
            return None

    """Remove uma chave da árvore, realizando merges ou redistribuições conforme necessário."""
    def remove(self, key: int) -> bool:
        leaf = self._find_leaf(key)
        try:
            idx = leaf.keys.index(key)
        except ValueError:
            return False

        # Remove chave e valor da folha
        leaf.keys.pop(idx)
        leaf.values.pop(idx)

        # Se a raiz ainda é folha, não precisa reequilibrar
        if leaf is self.root:
            self._snapshot(f"rem_{key}")
            return True

        # Reequilibra a partir dessa folha
        self._rebalance_after_delete(leaf)
        self._snapshot(f"rem_{key}")
        return True

    """Calcula o número mínimo de chaves que uma folha deve ter."""
    def _leaf_min_keys(self) -> int:
        return math.ceil((self.order - 1) / 2)

    """Calcula o número mínimo de chaves que um nó interno deve ter."""
    def _internal_min_keys(self) -> int:
        return math.ceil(self.order / 2) - 1

    """Obtém o pai, índice e irmãos esquerdo/direito de um nó."""
    def _get_siblings(self, node):
        parent = node.parent
        assert parent is not None
        idx = parent.children.index(node)
        left_sib = parent.children[idx - 1] if idx - 1 >= 0 else None
        right_sib = parent.children[idx + 1] if idx + 1 < len(parent.children) else None
        return parent, idx, left_sib, right_sib

    """Decide se precisa corrigir underflow na raiz, folha ou nó interno."""
    def _rebalance_after_delete(self, node):
        # Se chegou na raiz, pode reduzir a altura da árvore
        if node is self.root:
            if isinstance(node, InternalNode) and len(node.keys) == 0:
                child = node.children[0]
                child.parent = None
                self.root = child
            return
        # Nó não é raiz: trata underflow conforme o tipo
        if isinstance(node, LeafNode):
            self._fix_leaf_underflow(node)
        else:
            self._fix_internal_underflow(node)

    """Corrige underflow em um nó folha."""
    def _fix_leaf_underflow(self, leaf: 'LeafNode'):
        min_keys = self._leaf_min_keys()
        if len(leaf.keys) >= min_keys:
            return
        parent, idx, left_sib, right_sib = self._get_siblings(leaf)
        
        # 1) Tenta emprestar do irmão esquerdo
        if isinstance(left_sib, LeafNode) and len(left_sib.keys) > min_keys:
            k = left_sib.keys.pop()
            v = left_sib.values.pop()
            leaf.keys.insert(0, k)
            leaf.values.insert(0, v)
            parent.keys[idx - 1] = leaf.keys[0]
            return
        
        # 2) Tenta emprestar do irmão direito
        if isinstance(right_sib, LeafNode) and len(right_sib.keys) > min_keys:
            k = right_sib.keys.pop(0)
            v = right_sib.values.pop(0)
            leaf.keys.append(k)
            leaf.values.append(v)
            parent.keys[idx] = right_sib.keys[0]
            return
        
        # 3) Se não der pra emprestar, faz merge com irmão
        if isinstance(left_sib, LeafNode):
            # Merge: irmão esquerdo absorve esta folha
            left_sib.keys.extend(leaf.keys)
            left_sib.values.extend(leaf.values)
            left_sib.next_leaf = leaf.next_leaf
            del parent.keys[idx - 1]
            del parent.children[idx]
            self._rebalance_after_delete(parent)
        elif isinstance(right_sib, LeafNode):
            # Merge: esta folha absorve o irmão direito
            leaf.keys.extend(right_sib.keys)
            leaf.values.extend(right_sib.values)
            leaf.next_leaf = right_sib.next_leaf
            del parent.keys[idx]
            del parent.children[idx + 1]
            self._rebalance_after_delete(parent)

    """Corrige underflow em um nó interno."""
    def _fix_internal_underflow(self, node: 'InternalNode'):
        min_keys = self._internal_min_keys()
        if len(node.keys) >= min_keys:
            return
        parent, idx, left_sib, right_sib = self._get_siblings(node)
        
        # 1) Empresta do irmão esquerdo
        if isinstance(left_sib, InternalNode) and len(left_sib.keys) > min_keys:
            sep = parent.keys[idx - 1]
            borrow_key = left_sib.keys.pop()
            borrow_child = left_sib.children.pop()
            node.keys.insert(0, sep)
            node.children.insert(0, borrow_child)
            borrow_child.parent = node
            parent.keys[idx - 1] = borrow_key
            return
        
        # 2) Empresta do irmão direito
        if isinstance(right_sib, InternalNode) and len(right_sib.keys) > min_keys:
            sep = parent.keys[idx]
            borrow_key = right_sib.keys.pop(0)
            borrow_child = right_sib.children.pop(0)
            node.keys.append(sep)
            node.children.append(borrow_child)
            borrow_child.parent = node
            parent.keys[idx] = borrow_key
            return
        
        # 3) Não dá pra emprestar, faz merge com irmão
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
    
    """Exibe a estrutura da Árvore B+ de forma hierárquica."""
    def display(self):
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
        
    """Gera uma representação visual da Árvore B+ usando Graphviz."""
    def display_graphviz(self, filename_prefix="btree", out_dir="docs/imagens_btree", fmt="png"):
        os.makedirs(out_dir, exist_ok=True)
        g = Digraph("BPlusTree", format=fmt)
        g.attr("node", shape="record", fontname="Helvetica", fontsize="10")
        g.attr("edge", arrowsize="0.6")

        name_map = {}
        counter = {"i": 0}

        """Gera um nome único para cada nó."""
        def node_name(n):
            if n not in name_map:
                name_map[n] = f"n{counter['i']}"
                counter["i"] += 1
            return name_map[n]

        """Cria o rótulo do nó para o Graphviz."""
        def make_label(n):
            if isinstance(n, LeafNode):
                body = "|".join(str(k) for k in n.keys) if n.keys else "•"
                return f"{{Leaf|{body}}}"
            else:
                parts = []
                # porta para cada child: c0 k0 c1 k1 ... ck
                for i, k in enumerate(n.keys):
                    parts.append(f"<c{i}>")
                    parts.append(str(k))
                parts.append(f"<c{len(n.keys)}>")  # última porta
                return "{Internal|" + "|".join(parts) + "}"

        """Emite os nós e arestas recursivamente."""
        def emit(n):
            nid = node_name(n)
            g.node(nid, make_label(n))
            if isinstance(n, InternalNode):
                for i, ch in enumerate(n.children):
                    cid = node_name(ch)
                    g.node(cid, make_label(ch))
                    g.edge(f"{nid}:c{i}", cid)
                    emit(ch)

        emit(self.root)
        base = os.path.join(out_dir, f"{filename_prefix}")
        rendered_path = g.render(base, cleanup=True)  # ex.: docs/imagens_btree/btree.png
        print(f"Imagem gerada em: {rendered_path}")
        return rendered_path

    """Habilita a captura automática de snapshots após cada operação."""
    def enable_snapshots(self, prefix="btree", out_dir="docs/imagens_btree", fmt="png"):
        os.makedirs(out_dir, exist_ok=True)
        self._snap = {"prefix": prefix, "dir": out_dir, "fmt": fmt, "n": 0}

    """Tira um snapshot da árvore com o rótulo fornecido."""
    def _snapshot(self, label):
        if getattr(self, "_snap", None):
            n = self._snap["n"]
            fname = f"{self._snap['prefix']}_{n:03d}_{label}"
            self.display_graphviz(filename_prefix=fname, out_dir=self._snap["dir"], fmt=self._snap["fmt"])
            self._snap["n"] += 1