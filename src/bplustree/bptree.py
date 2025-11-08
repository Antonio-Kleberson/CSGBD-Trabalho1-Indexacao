import math

# --- 1. Classes Auxiliares (Nós) ---

class Node:
    """Nó base para nós internos e folhas."""
    def __init__(self, order: int):
        self.order = order # Ordem máxima de chaves
        self.keys = []
        self.parent = None
        # O número máximo de chaves é self.order - 1

    def is_full(self):
        """Verifica se o nó está cheio."""
        return len(self.keys) == self.order - 1

    def find_index(self, key):
        """Encontra o índice onde a chave deve ser inserida/buscada."""
        for i, k in enumerate(self.keys):
            if key < k:
                return i
        return len(self.keys)


class LeafNode(Node):
    """Nó folha: Armazena chaves e valores, e é encadeado."""
    def __init__(self, order: int):
        super().__init__(order)
        self.values = []
        self.next_leaf = None # Ponteiro para o próximo nó folha

    def add_key_value(self, key, value):
        """Insere um par (chave, valor) mantendo a ordem."""
        index = self.find_index(key)
        self.keys.insert(index, key)
        self.values.insert(index, value)

    def split(self):
        """Divide o nó folha em dois e retorna a chave promovida."""
        mid = math.ceil(len(self.keys) / 2)
        
        # Cria um novo nó folha
        new_leaf = LeafNode(self.order)
        
        # Move a metade direita para o novo nó
        new_leaf.keys = self.keys[mid:]
        new_leaf.values = self.values[mid:]
        
        # Remove a metade direita do nó original
        self.keys = self.keys[:mid]
        self.values = self.values[:mid]

        # Atualiza o encadeamento (lista ligada das folhas)
        new_leaf.next_leaf = self.next_leaf
        self.next_leaf = new_leaf

        # A chave a ser promovida para o pai é a menor chave do novo nó folha
        key_promoted = new_leaf.keys[0]
        
        return key_promoted, new_leaf


class InternalNode(Node):
    """Nó interno: Armazena chaves e ponteiros para filhos (outros nós)."""
    def __init__(self, order: int):
        super().__init__(order)
        # Lista de ponteiros para nós filhos (Nodes ou LeafNodes)
        self.children = [] 

    def add_key_child(self, key, child_node):
        """Adiciona uma chave e um nó filho, mantendo a ordem."""
        index = self.find_index(key)
        self.keys.insert(index, key)
        self.children.insert(index + 1, child_node)
        child_node.parent = self # Atualiza o ponteiro pai

    def split(self):
        """Divide o nó interno em dois e retorna a chave promovida."""
        mid = len(self.keys) // 2
        
        # A chave no meio é a chave que subirá e será REMOVIDA
        key_promoted = self.keys[mid]
        
        # Cria um novo nó interno
        new_node = InternalNode(self.order)
        
        # Move as chaves da direita (depois da chave promovida)
        new_node.keys = self.keys[mid + 1:]
        # Move os ponteiros filhos da direita (todos após o meio)
        new_node.children = self.children[mid + 1:]
        
        # Atualiza o nó original
        self.keys = self.keys[:mid]
        self.children = self.children[:mid + 1]

        # Atualiza os pais dos novos filhos
        for child in new_node.children:
            child.parent = new_node
            
        return key_promoted, new_node


# --- 2. Classe Principal da Árvore B+ ---

class BPlusTree:
    
    def __init__(self, order: int):
        """Inicializa a árvore com a ordem especificada."""
        # A ordem deve ser pelo menos 3 para ter sentido em um B-Tree
        if order < 3:
            raise ValueError("A ordem da Árvore B+ deve ser no mínimo 3.")
            
        self.order = order
        # A árvore começa com um nó folha como raiz
        self.root = LeafNode(order) 

    # --- Métodos de Navegação ---
    
    def _find_leaf(self, key) -> LeafNode:
        """Navega pelos nós internos até encontrar o nó folha correto."""
        node = self.root
        while not isinstance(node, LeafNode):
            # Encontra o índice da chave (para determinar qual filho seguir)
            index = node.find_index(key)
            node = node.children[index]
        return node
        
    # --- Método de Inserção ---

    def insert(self, key: int, value: any):
        """Insere um par (chave, valor) na árvore B+."""
        leaf = self._find_leaf(key)

        # 1. Adiciona o par (chave, valor) no nó folha
        leaf.add_key_value(key, value)
        
        # 2. Verifica se o nó folha precisa ser dividido
        if leaf.is_full():
            key_promoted, new_node = leaf.split()
            self._handle_split(leaf, key_promoted, new_node)

    def _handle_split(self, old_node: Node, key_promoted: int, new_node: Node):
        """Gerencia a promoção da chave e a divisão dos nós."""
        
        if old_node.parent is None:
            # Caso 1: A raiz está sendo dividida
            
            # Cria uma nova raiz (InternalNode)
            new_root = InternalNode(self.order)
            new_root.keys = [key_promoted]
            new_root.children = [old_node, new_node]
            
            # Atualiza os ponteiros pai
            old_node.parent = new_root
            new_node.parent = new_root
            
            # Atualiza a raiz da árvore
            self.root = new_root
            return

        # Caso 2: Nó interno está sendo dividido
        parent = old_node.parent
        
        # Adiciona a chave e o novo nó no pai
        parent.add_key_child(key_promoted, new_node)

        # Se o nó pai também ficar cheio, propaga a divisão
        if parent.is_full():
            key_parent_promoted, new_parent = parent.split()
            self._handle_split(parent, key_parent_promoted, new_parent)

    # --- Método de Busca ---

    def search(self, key: int) -> any:
        """Retorna o valor associado à chave, se existir."""
        leaf = self._find_leaf(key)
        
        # No nó folha, busca a chave e retorna o valor
        try:
            index = leaf.keys.index(key)
            return leaf.values[index]
        except ValueError:
            # Chave não encontrada no nó folha
            return None

    # --- Esboços de Métodos ---
    def remove(self, key: int) -> bool:
        """Remove a chave informada da árvore B+ (com borrow/merge)."""
        # 1) localiza a folha
        leaf = self._find_leaf(key)
        try:
            idx = leaf.keys.index(key)
        except ValueError:
            return False  # não existe

        # 2) remove (k,v) da folha
        leaf.keys.pop(idx)
        leaf.values.pop(idx)

        # 3) casos especiais da raiz
        if leaf is self.root:
            # raiz folha pode ficar vazia (árvore vazia) ou com poucas chaves
            return True

        # 4) reequilibra se necessário
        self._rebalance_after_delete(leaf)
        return True


        # ---------- limites mínimos ----------
    def _leaf_min_keys(self) -> int:
        # folhas: max chaves = order-1; mínimo ≈ ceil((order-1)/2)
        return math.ceil((self.order - 1) / 2)

    def _internal_min_keys(self) -> int:
        # internos: max chaves = order-1; min filhos = ceil(order/2)
        # min chaves = min filhos - 1 = ceil(order/2) - 1
        return math.ceil(self.order / 2) - 1

    # ---------- utilidades ----------
    def _get_siblings(self, node):
        """Retorna (parent, idx_no_parent, left_sib, right_sib)."""
        parent = node.parent
        assert parent is not None
        idx = parent.children.index(node)
        left_sib = parent.children[idx - 1] if idx - 1 >= 0 else None
        right_sib = parent.children[idx + 1] if idx + 1 < len(parent.children) else None
        return parent, idx, left_sib, right_sib

    # ---------- rebalance ----------
    def _rebalance_after_delete(self, node):
        """Reequilibra a partir de um nó (folha ou interno) que pode ter ficado abaixo do mínimo."""
        # redução de altura se a raiz for interna e ficar sem chaves
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

    # ---------- folhas: borrow/merge ----------
    def _fix_leaf_underflow(self, leaf: 'LeafNode'):
        min_keys = self._leaf_min_keys()
        if len(leaf.keys) >= min_keys:
            return  # nada a fazer

        parent, idx, left_sib, right_sib = self._get_siblings(leaf)

        # 1) emprestar do irmão esquerdo
        if isinstance(left_sib, LeafNode) and len(left_sib.keys) > min_keys:
            k = left_sib.keys.pop()
            v = left_sib.values.pop()
            leaf.keys.insert(0, k)
            leaf.values.insert(0, v)
            # separador entre left_sib e leaf vira a 1ª chave do leaf
            parent.keys[idx - 1] = leaf.keys[0]
            return

        # 2) emprestar do irmão direito
        if isinstance(right_sib, LeafNode) and len(right_sib.keys) > min_keys:
            k = right_sib.keys.pop(0)
            v = right_sib.values.pop(0)
            leaf.keys.append(k)
            leaf.values.append(v)
            # separador entre leaf e right_sib vira a 1ª chave do right_sib
            parent.keys[idx] = right_sib.keys[0]
            return

        # 3) merge
        if isinstance(left_sib, LeafNode):
            # left <- leaf
            left_sib.keys.extend(leaf.keys)
            left_sib.values.extend(leaf.values)
            left_sib.next_leaf = leaf.next_leaf
            # remove separador correspondente no pai
            del parent.keys[idx - 1]
            del parent.children[idx]
            self._rebalance_after_delete(parent)
        elif isinstance(right_sib, LeafNode):
            # leaf <- right
            leaf.keys.extend(right_sib.keys)
            leaf.values.extend(right_sib.values)
            leaf.next_leaf = right_sib.next_leaf
            del parent.keys[idx]
            del parent.children[idx + 1]
            self._rebalance_after_delete(parent)

    # ---------- internos: borrow/merge ----------
    def _fix_internal_underflow(self, node: 'InternalNode'):
        min_keys = self._internal_min_keys()
        if len(node.keys) >= min_keys:
            return

        parent, idx, left_sib, right_sib = self._get_siblings(node)

        # 1) emprestar do irmão esquerdo
        if isinstance(left_sib, InternalNode) and len(left_sib.keys) > min_keys:
            sep = parent.keys[idx - 1]
            borrow_key = left_sib.keys.pop()
            borrow_child = left_sib.children.pop()
            node.keys.insert(0, sep)
            node.children.insert(0, borrow_child)
            borrow_child.parent = node
            parent.keys[idx - 1] = borrow_key
            return

        # 2) emprestar do irmão direito
        if isinstance(right_sib, InternalNode) and len(right_sib.keys) > min_keys:
            sep = parent.keys[idx]
            borrow_key = right_sib.keys.pop(0)
            borrow_child = right_sib.children.pop(0)
            node.keys.append(sep)
            node.children.append(borrow_child)
            borrow_child.parent = node
            parent.keys[idx] = borrow_key
            return

        # 3) merge
        if isinstance(left_sib, InternalNode):
            # left <- (sep do pai) <- node
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
            # node <- (sep do pai) <- right
            sep = parent.keys[idx]
            node.keys.append(sep)
            node.keys.extend(right_sib.keys)
            node.children.extend(right_sib.children)
            for ch in right_sib.children:
                ch.parent = node
            del parent.keys[idx]
            del parent.children[idx + 1]
            self._rebalance_after_delete(parent)