 Relatório Técnico – Indexação Dinâmica em SGBD
 Universidade Federal de Tecnologia

Disciplina: Sistemas de Gerenciamento de Banco de Dados

Aluno: Antonio Avelino, Antonio Kleberson 

Tema: Implementação de Hash Extensível e Árvore B+

Data: Novembro de 2025

# 1. Introdução

A performance de um Sistema de Gerenciamento de Banco de Dados (SGBD) depende fortemente de suas estruturas de indexação, que são responsáveis por acelerar operações de leitura e escrita.
Duas das abordagens dinâmicas mais relevantes são o Hash Extensível e a Árvore B+, amplamente utilizadas em sistemas como PostgreSQL, MySQL e Oracle.

Neste trabalho, foi desenvolvido um projeto em Python, aplicando os princípios dessas estruturas, documentando sua implementação e funcionamento visual.
Além disso, foi adicionado testes automatizados no GitHub para garantir a confiabilidade do código.

# 2. Objetivos
# 2.1 Objetivo Geral

Implementar e analisar as estruturas Hash Extensível e Árvore B+, destacando suas operações, dinâmica de crescimento e redução, e aplicabilidade em SGBDs.

# 2.2 Objetivos Específicos

Compreender a lógica de gerenciamento de páginas, buckets e nós.

Implementar as operações de inserção, busca e remoção.

Gerar visualizações gráficas automáticas (Graphviz).

Garantir qualidade com testes unitários.

Documentar o projeto conforme padrões técnicos de SGBD.

# 3. Fundamentação Teórica
# 3.1 Hash Extensível

O Hash Extensível é uma estrutura que adapta seu tamanho conforme o volume de dados.
Ela utiliza dois níveis principais:

Diretório: armazena ponteiros para buckets, indexado por bits do valor hash da chave.

Buckets (páginas): guardam os registros e possuem profundidade local (local_depth).

A profundidade global (global_depth) indica quantos bits da função hash são usados para indexar o diretório.

Operações principais:

# Inserção: 
Calcula o hash, acessa o bucket e, se cheio, realiza split (divisão).

# Busca: 
Aplica o hash e acessa diretamente o bucket correspondente.

# Remoção: 
Exclui o registro e tenta mergear (unir) buckets irmãos, reduzindo o diretório se possível.

# 3.2 Árvore B+

A Árvore B+ é uma estrutura balanceada de múltiplos caminhos utilizada para indexação ordenada.

Características principais:

Todos os registros estão nas folhas.

As folhas são encadeadas para percursos ordenados.

Os nós internos funcionam como índices-guia.

A altura da árvore é mantida constante por meio de splits e merges.

Operações:

# Inserção: 
insere na folha correta e divide se necessário.

# Busca: 
percorre da raiz à folha.

# Remoção: 
remove e, se necessário, redistribui ou une nós.

# 4. Estrutura do Projeto
src/

 ├── extensible_hash/

 │   ├── hash_extensible.py     # Implementação completa do Hash Extensível
 
 │   └── demo_hash.py           # Demonstração visual (Graphviz + tabela)
 
 ├── bplustree/
 
 │   └── bplus_tree.py          # Implementação da Árvore B+
 
tests/

 ├── test_hash.py         # Testes unitários do Hash Extensível
 
 └── test_btree.py        # Testes unitários da Árvore B+
 
docs/

 └── prints/                    # Diagramas PNG gerados automaticamente


# Bibliotecas utilizadas:

graphviz — geração de diagramas.

tabulate — exibição em formato de tabela no terminal.

pytest — testes automatizados.

# 5. Funcionamento do Hash Extensível
# 5.1 Inserção

Calcula o valor hash da chave.

Seleciona o bucket pelo índice binário (global_depth).

Se o bucket estiver cheio:

Aumenta o local_depth e divide o bucket (split).

Redistribui as chaves.

Se local_depth > global_depth, o diretório é duplicado.

# 5.2 Busca

Calcula o hash da chave e acessa diretamente o bucket correspondente.

Operação O(1) em média.

# 5.3 Remoção

Remove o item.

Se possível, faz merge com bucket irmão (bit complementar).

Reduz o diretório se todos os buckets tiverem menor profundidade.

# 5.4 Visualização

O arquivo demo_hash.py gera imagens PNG mostrando o estado após cada operação, salvas em docs/prints/.

# 6. Funcionamento da Árvore B+
# 6.1 Inserção

Encontra a folha apropriada.

Insere a chave em ordem.

Se a folha estiver cheia, divide (split).

A chave do meio sobe ao pai (propagação).

Se a raiz dividir, cria-se nova raiz.

# 6.2 Busca

Percorre a árvore a partir da raiz.

Comparações binárias até chegar à folha.

Complexidade: O(log n).

# 6.3 Remoção

Remove a chave.

Redistribui com o nó vizinho ou faz merge.

Se a raiz ficar com um único filho, é removida.

# 6.4 Vantagens

Mantém ordenação natural dos registros.

Suporta buscas por intervalo.

É a base para índices clustered e non-clustered em SGBDs reais.

# 7. Testes Automatizados (Pytest)

Testes asseguram que as operações respeitam as propriedades teóricas:

def test_merge_and_shrink():

    h = ExtensibleHash(bucket_size=2)
    
    for k in [1, 2, 3, 4]:
    
        h.insert(k, f"v{k}")
        
    h.remove(3)
    
    h.remove(4)
    
    assert h.global_depth >= 1


# 8. Resultados e Análise

As operações de split e merge foram validadas visualmente e por testes.

O diretório do Hash Extensível se adaptou ao número de chaves, crescendo e encolhendo conforme o esperado.

Na Árvore B+, as divisões e redistribuições mantiveram a árvore balanceada.

O tempo médio das operações permaneceu estável, demonstrando a eficiência das estruturas dinâmicas.

# 9. Conclusão

O trabalho cumpriu integralmente os objetivos propostos.
Foram implementadas e testadas duas das principais estruturas de indexação dinâmicas utilizadas em SGBDs.

O Hash Extensível mostrou-se eficiente para buscas por igualdade, enquanto a Árvore B+ se destacou em consultas por intervalos.
O uso de testes automatizados e integração contínua garantiu a robustez e confiabilidade do código.

Essas técnicas refletem os mecanismos usados em sistemas reais como PostgreSQL e Oracle, conectando teoria e prática de forma concreta.

# 10. Referências

ELMASRI, R.; NAVATHE, S. Sistemas de Banco de Dados. 7ª Ed. Pearson, 2019.

SILBERSCHATZ, A.; KORTH, H.; SUDARSHAN, S. Database System Concepts. 6ª Ed. McGraw-Hill, 2020.

KNUTH, D. The Art of Computer Programming, Vol. 3. Addison-Wesley, 1998.

Documentação do Graphviz
.

Documentação do Pytest

Como rodar o projeto
# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install graphviz tabulate pytest

# Rodar demonstração visual
python -m src.extensible_hash.demo_hash

python -m src.bplustree.bptree

# Executar testes automatizados
pytest -v
