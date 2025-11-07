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


