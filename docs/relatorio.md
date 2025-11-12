<!-- 1. Introdução

A indexação é um dos pilares de desempenho em Sistemas de Gerenciamento de Banco de Dados (SGBD).
Ela permite que o sistema localize registros de maneira rápida, sem percorrer toda a tabela, reduzindo custos de acesso ao disco.

Duas estruturas amplamente utilizadas para esse fim são o Hash Extensível e a Árvore B+, ambas capazes de se adaptar dinamicamente à inserção e remoção de dados, mantendo desempenho e eficiência no uso de espaço.

Este relatório apresenta a implementação prática dessas duas técnicas em Python, com visualização gráfica, testes automatizados e análise comparativa de comportamento.

2. Objetivos
2.1 Objetivo Geral

Implementar e analisar as estruturas de Hash Extensível e Árvore B+, destacando suas operações de inserção, busca, remoção e gerenciamento de blocos.

2.2 Objetivos Específicos

Demonstrar o funcionamento dinâmico do crescimento (split) e redução (merge) das estruturas.

Validar o comportamento por meio de testes automatizados e visualizações gráficas.

Comparar o desempenho teórico e prático entre as duas abordagens de indexação.

Documentar a implementação seguindo boas práticas de engenharia de software e SGBD.

3. Fundamentação Teórica
3.1 Hash Extensível

O Hash Extensível é uma técnica de hashing dinâmico em que a tabela cresce e diminui conforme o número de registros.

O diretório contém ponteiros para buckets.

Cada bucket tem uma profundidade local, e o diretório tem uma profundidade global.

Quando um bucket enche, ele é dividido (split).

Se necessário, o diretório é duplicado.

Quando buckets esvaziam, podem ser fundidos (merge), e o diretório pode ser reduzido (shrink).

Operações:

Inserção: calcula-se o hash, localiza-se o bucket e, se cheio, divide-se.

Busca: aplica-se a função hash e acessa-se diretamente o bucket.

Remoção: elimina o registro e tenta mergear buckets irmãos.

Complexidade média: O(1).

3.2 Árvore B+

A Árvore B+ é uma estrutura de indexação balanceada, amplamente utilizada em bancos de dados para consultas ordenadas e por intervalo.

Todos os registros estão nas folhas.

As folhas são ligadas sequencialmente, facilitando varreduras ordenadas.

A árvore se mantém balanceada — todas as folhas estão no mesmo nível.

Cada nó interno contém chaves-guia e ponteiros para subárvores.

Operações:

Inserção: insere em uma folha; se cheia, divide e propaga para cima.

Busca: percorre da raiz até a folha, comparando chaves.

Remoção: retira a chave, e se o nó cair abaixo do limite, redistribui ou mergeia.

Complexidade média: O(log n).

4. Implementação
4.1 Estrutura de pastas
src/
 ├── extensible_hash/
 │   ├── hash_extensible.py
 │   └── demo_hash.py
 └── bplustree/
     └── btree.py
tests/
 ├── test_hash.py
 └── test_bptree.py
 └── test_bptree_merge.py
docs/
 └── prints/

4.2 Tecnologias e Ferramentas

Python 3.12 — linguagem de implementação.

Graphviz — geração automática de diagramas das estruturas.

Tabulate — exibição tabular no terminal.

Pytest — execução automatizada de testes.

GitHub Actions — integração contínua (CI).

5. Fluxo de Execução

O arquivo demo_hash.py executa as quatro operações principais:

Inserção de chaves e geração de imagens (docs/prints/insert_XX.png);

Busca de chaves específicas;

Remoção de chaves com merge e shrink;

Exibição tabular do estado da hash após cada operação.

Exemplo visual (modo texto):

| Índice | Bucket    | Conteúdo                    |
|---------|-----------|-----------------------------|
| 00      | B0 (ld=1) | (1, valor_1), (3, valor_3)  |
| 01      | B0 (ld=1) | (1, valor_1), (3, valor_3)  |
| 10      | B1 (ld=1) | (2, valor_2)                |
| 11      | B1 (ld=1) | (2, valor_2)                |
Profundidade Global: 2

6. Testes Automatizados
6.1 Testes Unitários

Os testes foram criados com pytest para validar todas as operações da estrutura.

Exemplo:

def test_merge_and_shrink():
    h = ExtensibleHash(bucket_size=2)
    for k in [1, 2, 3, 4]:
        h.insert(k, f"v{k}")
    h.remove(3)
    h.remove(4)
    assert h.global_depth >= 1

7. Resultados e Análise

Durante a execução:

Os splits ocorreram de forma localizada, sem reestruturação completa.

O merge e o shrink reduziram corretamente o diretório após remoções.

A estrutura mostrou-se eficiente e previsível.

As imagens geradas pelo Graphviz mostraram a evolução do diretório e dos buckets, facilitando o entendimento visual.

8. Conclusão

O trabalho demonstrou com sucesso o funcionamento dinâmico das estruturas Hash Extensível e Árvore B+, aplicando conceitos teóricos de indexação de dados e técnicas de engenharia de software moderna (testes e CI).

O projeto atingiu todos os objetivos propostos, combinando:

rigor técnico;

clareza visual;

documentação completa;

automação de validação.

Essa integração de teoria, prática e automação reflete os princípios fundamentais do desenvolvimento de Sistemas de Banco de Dados de alto desempenho. -->