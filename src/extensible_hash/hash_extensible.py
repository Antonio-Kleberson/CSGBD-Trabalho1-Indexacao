# src/extensible_hash/hash_extensible.py

class ExtensibleHash:
    """
    Implementação base da Tabela Hash Extensível.

    A estrutura mantém um diretório de ponteiros para buckets.
    Cada bucket possui uma profundidade local e uma capacidade máxima de registros.
    A profundidade global define quantos bits são usados da função hash.

    Operações básicas:
    - insert(key, value): insere um novo par (chave, valor).
    - search(key): busca um valor associado à chave.
    - remove(key): remove o registro da estrutura.
    - display(): exibe o diretório e os buckets.
    """

    def __init__(self, bucket_size: int):
        """
        Inicializa a tabela hash com o tamanho máximo de registros por bucket.
        :param bucket_size: capacidade máxima de registros por bucket.
        """
        pass

    def insert(self, key: int, value: any):
        """
        Insere um par (chave, valor) na estrutura.
        :param key: chave inteira.
        :param value: valor associado.
        """
        pass

    def search(self, key: int) -> any:
        """
        Retorna o valor associado à chave, se existir.
        :param key: chave a ser buscada.
        :return: valor encontrado ou None.
        """
        pass

    def remove(self, key: int) -> bool:
        """
        Remove o registro com a chave informada.
        :param key: chave a ser removida.
        :return: True se foi removido; False se não foi encontrado.
        """
        pass

    def display(self):
        """
        Exibe o diretório e os buckets da tabela hash.
        Útil para depuração e visualização da estrutura.
        """
        pass
