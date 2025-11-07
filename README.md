# Trabalho - Indexação (Hash Extensível e Árvore B+)

Repositório do trabalho da disciplina **SGBD**.

##  Objetivo
Implementar e comparar duas estruturas de indexação:
- **Hash Extensível**
- **Árvore B+**

Com as operações: inserir, buscar, remover e exibir.

##  Linguagem
O projeto será desenvolvido em **Python 3.x**, com código modular, exemplos de uso e testes automatizados.

##  Execução
```bash hash_extensible.py
python -m src.extensible_hash.demo_hash
```


## Autores

Nome: Antonio Avelino, Antonio Kleberson

Curso: Sistema de Informação

Disciplina: Sistemas de Gerenciamento de Banco de Dados

Saídas do terminal

```bash
==== Demonstração da Tabela Hash Extensível ====

=== INSERÇÕES ===

Inserindo chave 1...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 1
0 → B0 Bucket(ld=1, items=[(1, 'valor_1')])
1 → B0 Bucket(ld=1, items=[(1, 'valor_1')])
=======================================


|   Índice | Bucket    | Conteúdo     |
|----------|-----------|--------------|
|        0 | B0 (ld=1) | (1, valor_1) |
|        1 | B0 (ld=1) | (1, valor_1) |
Profundidade Global: 1

[✓] Diagrama gerado: docs/prints/insert_01.png

Inserindo chave 2...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 1
0 → B0 Bucket(ld=1, items=[(1, 'valor_1'), (2, 'valor_2')])
1 → B0 Bucket(ld=1, items=[(1, 'valor_1'), (2, 'valor_2')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|        0 | B0 (ld=1) | (1, valor_1), (2, valor_2) |
|        1 | B0 (ld=1) | (1, valor_1), (2, valor_2) |
Profundidade Global: 1

[✓] Diagrama gerado: docs/prints/insert_02.png

Inserindo chave 3...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 2
00 → B0 Bucket(ld=2, items=[(1, 'valor_1')])
01 → B0 Bucket(ld=2, items=[(1, 'valor_1')])
10 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|       00 | B0 (ld=2) | (1, valor_1)               |
|       01 | B0 (ld=2) | (1, valor_1)               |
|       10 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|       11 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
Profundidade Global: 2

[✓] Diagrama gerado: docs/prints/insert_03.png

Inserindo chave 4...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 2
00 → B0 Bucket(ld=2, items=[(1, 'valor_1'), (4, 'valor_4')])
01 → B0 Bucket(ld=2, items=[(1, 'valor_1'), (4, 'valor_4')])
10 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|       00 | B0 (ld=2) | (1, valor_1), (4, valor_4) |
|       01 | B0 (ld=2) | (1, valor_1), (4, valor_4) |
|       10 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|       11 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
Profundidade Global: 2

[✓] Diagrama gerado: docs/prints/insert_04.png

Inserindo chave 5...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 3
000 → B0 Bucket(ld=3, items=[(1, 'valor_1')])
001 → B0 Bucket(ld=3, items=[(1, 'valor_1')])
010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
100 → B2 Bucket(ld=3, items=[(4, 'valor_4'), (5, 'valor_5')])
101 → B2 Bucket(ld=3, items=[(4, 'valor_4'), (5, 'valor_5')])
110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|      000 | B0 (ld=3) | (1, valor_1)               |
|      001 | B0 (ld=3) | (1, valor_1)               |
|      010 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      011 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      100 | B2 (ld=3) | (4, valor_4), (5, valor_5) |
|      101 | B2 (ld=3) | (4, valor_4), (5, valor_5) |
|      110 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      111 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
Profundidade Global: 3

[✓] Diagrama gerado: docs/prints/insert_05.png

Inserindo chave 8...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 3
000 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
001 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
100 → B2 Bucket(ld=3, items=[(4, 'valor_4'), (5, 'valor_5')])
101 → B2 Bucket(ld=3, items=[(4, 'valor_4'), (5, 'valor_5')])
110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|      000 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|      001 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|      010 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      011 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      100 | B2 (ld=3) | (4, valor_4), (5, valor_5) |
|      101 | B2 (ld=3) | (4, valor_4), (5, valor_5) |
|      110 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|      111 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
Profundidade Global: 3

[✓] Diagrama gerado: docs/prints/insert_06.png

Inserindo chave 12...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
0001 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
0010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0100 → B2 Bucket(ld=4, items=[(4, 'valor_4'), (5, 'valor_5')])
0101 → B2 Bucket(ld=4, items=[(4, 'valor_4'), (5, 'valor_5')])
0110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1000 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
1001 → B0 Bucket(ld=3, items=[(1, 'valor_1'), (8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1100 → B3 Bucket(ld=4, items=[(12, 'valor_12')])
1101 → B3 Bucket(ld=4, items=[(12, 'valor_12')])
1110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                   |
|----------|-----------|----------------------------|
|     0000 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|     0001 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|     0010 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     0011 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     0100 | B2 (ld=4) | (4, valor_4), (5, valor_5) |
|     0101 | B2 (ld=4) | (4, valor_4), (5, valor_5) |
|     0110 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     0111 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     1000 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|     1001 | B0 (ld=3) | (1, valor_1), (8, valor_8) |
|     1010 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     1011 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     1100 | B3 (ld=4) | (12, valor_12)             |
|     1101 | B3 (ld=4) | (12, valor_12)             |
|     1110 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
|     1111 | B1 (ld=2) | (2, valor_2), (3, valor_3) |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/insert_07.png

Inserindo chave 16...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0100 → B2 Bucket(ld=4, items=[(4, 'valor_4'), (5, 'valor_5')])
0101 → B2 Bucket(ld=4, items=[(4, 'valor_4'), (5, 'valor_5')])
0110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
0111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
1111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|     0000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     0011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     0100 | B2 (ld=4) | (4, valor_4), (5, valor_5)   |
|     0101 | B2 (ld=4) | (4, valor_4), (5, valor_5)   |
|     0110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     0111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     1000 | B3 (ld=4) | (8, valor_8)                 |
|     1001 | B3 (ld=4) | (8, valor_8)                 |
|     1010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     1011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     1100 | B4 (ld=4) | (12, valor_12)               |
|     1101 | B4 (ld=4) | (12, valor_12)               |
|     1110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|     1111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/insert_08.png

Inserindo chave 20...

===== Estado Atual da Tabela Hash =====
Profundidade Global: 5
00000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
00001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
00010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
00011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
00100 → B2 Bucket(ld=5, items=[(4, 'valor_4'), (5, 'valor_5')])
00101 → B2 Bucket(ld=5, items=[(4, 'valor_4'), (5, 'valor_5')])
00110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
00111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
01000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
01001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
01010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
01011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
01100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
01101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
01110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
01111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
10000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
10001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
10010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
10011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
10100 → B5 Bucket(ld=5, items=[(20, 'valor_20')])
10101 → B5 Bucket(ld=5, items=[(20, 'valor_20')])
10110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
10111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
11001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
11010 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11011 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
11101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
11110 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
11111 → B1 Bucket(ld=2, items=[(2, 'valor_2'), (3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|    00000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    00001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    00010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    00011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    00100 | B2 (ld=5) | (4, valor_4), (5, valor_5)   |
|    00101 | B2 (ld=5) | (4, valor_4), (5, valor_5)   |
|    00110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    00111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    01000 | B3 (ld=4) | (8, valor_8)                 |
|    01001 | B3 (ld=4) | (8, valor_8)                 |
|    01010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    01011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    01100 | B4 (ld=4) | (12, valor_12)               |
|    01101 | B4 (ld=4) | (12, valor_12)               |
|    01110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    01111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    10000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    10001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    10010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    10011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    10100 | B5 (ld=5) | (20, valor_20)               |
|    10101 | B5 (ld=5) | (20, valor_20)               |
|    10110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    10111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    11000 | B3 (ld=4) | (8, valor_8)                 |
|    11001 | B3 (ld=4) | (8, valor_8)                 |
|    11010 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    11011 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    11100 | B4 (ld=4) | (12, valor_12)               |
|    11101 | B4 (ld=4) | (12, valor_12)               |
|    11110 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
|    11111 | B1 (ld=2) | (2, valor_2), (3, valor_3)   |
Profundidade Global: 5

[✓] Diagrama gerado: docs/prints/insert_09.png

-- Inserções concluídas --


=== BUSCAS ===
Chave 1 encontrada → valor_1
Chave 4 encontrada → valor_4
Chave 6 não encontrada!
Chave 10 não encontrada!

-- Buscas concluídas --


=== REMOÇÕES ===
Chave 2: Removido

===== Estado Atual da Tabela Hash =====
Profundidade Global: 5
00000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
00001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
00010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
00011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
00100 → B2 Bucket(ld=5, items=[(4, 'valor_4'), (5, 'valor_5')])
00101 → B2 Bucket(ld=5, items=[(4, 'valor_4'), (5, 'valor_5')])
00110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
00111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
01000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
01001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
01010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
01011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
01100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
01101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
01110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
01111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
10000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
10001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
10010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
10011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
10100 → B5 Bucket(ld=5, items=[(20, 'valor_20')])
10101 → B5 Bucket(ld=5, items=[(20, 'valor_20')])
10110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
10111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
11000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
11001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
11010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
11011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
11100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
11101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
11110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
11111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|    00000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    00001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    00010 | B1 (ld=2) | (3, valor_3)                 |
|    00011 | B1 (ld=2) | (3, valor_3)                 |
|    00100 | B2 (ld=5) | (4, valor_4), (5, valor_5)   |
|    00101 | B2 (ld=5) | (4, valor_4), (5, valor_5)   |
|    00110 | B1 (ld=2) | (3, valor_3)                 |
|    00111 | B1 (ld=2) | (3, valor_3)                 |
|    01000 | B3 (ld=4) | (8, valor_8)                 |
|    01001 | B3 (ld=4) | (8, valor_8)                 |
|    01010 | B1 (ld=2) | (3, valor_3)                 |
|    01011 | B1 (ld=2) | (3, valor_3)                 |
|    01100 | B4 (ld=4) | (12, valor_12)               |
|    01101 | B4 (ld=4) | (12, valor_12)               |
|    01110 | B1 (ld=2) | (3, valor_3)                 |
|    01111 | B1 (ld=2) | (3, valor_3)                 |
|    10000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    10001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|    10010 | B1 (ld=2) | (3, valor_3)                 |
|    10011 | B1 (ld=2) | (3, valor_3)                 |
|    10100 | B5 (ld=5) | (20, valor_20)               |
|    10101 | B5 (ld=5) | (20, valor_20)               |
|    10110 | B1 (ld=2) | (3, valor_3)                 |
|    10111 | B1 (ld=2) | (3, valor_3)                 |
|    11000 | B3 (ld=4) | (8, valor_8)                 |
|    11001 | B3 (ld=4) | (8, valor_8)                 |
|    11010 | B1 (ld=2) | (3, valor_3)                 |
|    11011 | B1 (ld=2) | (3, valor_3)                 |
|    11100 | B4 (ld=4) | (12, valor_12)               |
|    11101 | B4 (ld=4) | (12, valor_12)               |
|    11110 | B1 (ld=2) | (3, valor_3)                 |
|    11111 | B1 (ld=2) | (3, valor_3)                 |
Profundidade Global: 5

[✓] Diagrama gerado: docs/prints/remove_01.png
Chave 5: Removido

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
0011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
0100 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0101 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
0111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
1000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
1011 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
1100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1110 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
1111 → B1 Bucket(ld=2, items=[(3, 'valor_3')])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|     0000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0010 | B1 (ld=2) | (3, valor_3)                 |
|     0011 | B1 (ld=2) | (3, valor_3)                 |
|     0100 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0101 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0110 | B1 (ld=2) | (3, valor_3)                 |
|     0111 | B1 (ld=2) | (3, valor_3)                 |
|     1000 | B3 (ld=4) | (8, valor_8)                 |
|     1001 | B3 (ld=4) | (8, valor_8)                 |
|     1010 | B1 (ld=2) | (3, valor_3)                 |
|     1011 | B1 (ld=2) | (3, valor_3)                 |
|     1100 | B4 (ld=4) | (12, valor_12)               |
|     1101 | B4 (ld=4) | (12, valor_12)               |
|     1110 | B1 (ld=2) | (3, valor_3)                 |
|     1111 | B1 (ld=2) | (3, valor_3)                 |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/remove_02.png
Chave 3: Removido

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0010 → B1 Bucket(ld=2, items=[])
0011 → B1 Bucket(ld=2, items=[])
0100 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0101 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0110 → B1 Bucket(ld=2, items=[])
0111 → B1 Bucket(ld=2, items=[])
1000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[])
1011 → B1 Bucket(ld=2, items=[])
1100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1110 → B1 Bucket(ld=2, items=[])
1111 → B1 Bucket(ld=2, items=[])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|     0000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0010 | B1 (ld=2) | vazio                        |
|     0011 | B1 (ld=2) | vazio                        |
|     0100 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0101 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0110 | B1 (ld=2) | vazio                        |
|     0111 | B1 (ld=2) | vazio                        |
|     1000 | B3 (ld=4) | (8, valor_8)                 |
|     1001 | B3 (ld=4) | (8, valor_8)                 |
|     1010 | B1 (ld=2) | vazio                        |
|     1011 | B1 (ld=2) | vazio                        |
|     1100 | B4 (ld=4) | (12, valor_12)               |
|     1101 | B4 (ld=4) | (12, valor_12)               |
|     1110 | B1 (ld=2) | vazio                        |
|     1111 | B1 (ld=2) | vazio                        |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/remove_03.png
Chave 7: Não encontrado

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0010 → B1 Bucket(ld=2, items=[])
0011 → B1 Bucket(ld=2, items=[])
0100 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0101 → B2 Bucket(ld=4, items=[(20, 'valor_20'), (4, 'valor_4')])
0110 → B1 Bucket(ld=2, items=[])
0111 → B1 Bucket(ld=2, items=[])
1000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[])
1011 → B1 Bucket(ld=2, items=[])
1100 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1101 → B4 Bucket(ld=4, items=[(12, 'valor_12')])
1110 → B1 Bucket(ld=2, items=[])
1111 → B1 Bucket(ld=2, items=[])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|     0000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0010 | B1 (ld=2) | vazio                        |
|     0011 | B1 (ld=2) | vazio                        |
|     0100 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0101 | B2 (ld=4) | (20, valor_20), (4, valor_4) |
|     0110 | B1 (ld=2) | vazio                        |
|     0111 | B1 (ld=2) | vazio                        |
|     1000 | B3 (ld=4) | (8, valor_8)                 |
|     1001 | B3 (ld=4) | (8, valor_8)                 |
|     1010 | B1 (ld=2) | vazio                        |
|     1011 | B1 (ld=2) | vazio                        |
|     1100 | B4 (ld=4) | (12, valor_12)               |
|     1101 | B4 (ld=4) | (12, valor_12)               |
|     1110 | B1 (ld=2) | vazio                        |
|     1111 | B1 (ld=2) | vazio                        |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/remove_04.png
Chave 12: Removido

===== Estado Atual da Tabela Hash =====
Profundidade Global: 4
0000 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0001 → B0 Bucket(ld=4, items=[(1, 'valor_1'), (16, 'valor_16')])
0010 → B1 Bucket(ld=2, items=[])
0011 → B1 Bucket(ld=2, items=[])
0100 → B2 Bucket(ld=3, items=[(20, 'valor_20'), (4, 'valor_4')])
0101 → B2 Bucket(ld=3, items=[(20, 'valor_20'), (4, 'valor_4')])
0110 → B1 Bucket(ld=2, items=[])
0111 → B1 Bucket(ld=2, items=[])
1000 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1001 → B3 Bucket(ld=4, items=[(8, 'valor_8')])
1010 → B1 Bucket(ld=2, items=[])
1011 → B1 Bucket(ld=2, items=[])
1100 → B2 Bucket(ld=3, items=[(20, 'valor_20'), (4, 'valor_4')])
1101 → B2 Bucket(ld=3, items=[(20, 'valor_20'), (4, 'valor_4')])
1110 → B1 Bucket(ld=2, items=[])
1111 → B1 Bucket(ld=2, items=[])
=======================================


|   Índice | Bucket    | Conteúdo                     |
|----------|-----------|------------------------------|
|     0000 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0001 | B0 (ld=4) | (1, valor_1), (16, valor_16) |
|     0010 | B1 (ld=2) | vazio                        |
|     0011 | B1 (ld=2) | vazio                        |
|     0100 | B2 (ld=3) | (20, valor_20), (4, valor_4) |
|     0101 | B2 (ld=3) | (20, valor_20), (4, valor_4) |
|     0110 | B1 (ld=2) | vazio                        |
|     0111 | B1 (ld=2) | vazio                        |
|     1000 | B3 (ld=4) | (8, valor_8)                 |
|     1001 | B3 (ld=4) | (8, valor_8)                 |
|     1010 | B1 (ld=2) | vazio                        |
|     1011 | B1 (ld=2) | vazio                        |
|     1100 | B2 (ld=3) | (20, valor_20), (4, valor_4) |
|     1101 | B2 (ld=3) | (20, valor_20), (4, valor_4) |
|     1110 | B1 (ld=2) | vazio                        |
|     1111 | B1 (ld=2) | vazio                        |
Profundidade Global: 4

[✓] Diagrama gerado: docs/prints/remove_05.png

-- Remoções concluídas --

==== Demonstração finalizada ====
```