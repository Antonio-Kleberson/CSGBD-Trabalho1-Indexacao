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


