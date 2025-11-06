# src/extensible_hash/demo_hash.py
from .hash_extensible import ExtensibleHash
from graphviz import Digraph
import os
from tabulate import tabulate


def visualizar_hash(hash_table, step_name="hash_step"):
    """Gera uma imagem PNG da estrutura atual da tabela hash usando Graphviz."""
    dot = Digraph(comment=f"Extensible Hash - {step_name}")
    dot.attr(rankdir='LR', size='8,5')

    seen = {}
    for i, b in enumerate(hash_table.directory):
        dir_label = f"dir[{i:0{hash_table.global_depth}b}]"
        dot.node(dir_label, dir_label, shape="ellipse", color="black")

        if id(b) not in seen:
            seen[id(b)] = f"B{len(seen)}"
            bucket_label = seen[id(b)]
            conteudo = "\\n".join([f"{k}:{v}" for k, v in b.items]) or "(vazio)"
            dot.node(bucket_label,
                    f"{bucket_label}\\nld={b.local_depth}\\n{conteudo}",
                    shape="box", style="filled", color="lightblue")

        dot.edge(dir_label, seen[id(b)])

    os.makedirs("docs/prints", exist_ok=True)
    output_path = f"docs/prints/{step_name}"
    dot.render(output_path, format="png", cleanup=True)
    print(f"[✓] Diagrama gerado: {output_path}.png")


def mostrar_tabela(hash_table):
    """Mostra o estado atual da hash extensível em formato tabular (terminal/Markdown)."""
    data = []
    seen = {}
    for i, b in enumerate(hash_table.directory):
        idx_bin = f"{i:0{hash_table.global_depth}b}"
        if id(b) not in seen:
            seen[id(b)] = f"B{len(seen)}"
        bucket_label = f"{seen[id(b)]} (ld={b.local_depth})"
        conteudo = ", ".join(f"({k}, {v})" for k, v in b.items) or "vazio"
        data.append([idx_bin, bucket_label, conteudo])

    print("\n" + tabulate(data, headers=["Índice", "Bucket", "Conteúdo"], tablefmt="github"))
    print(f"Profundidade Global: {hash_table.global_depth}\n")


def demo_insert(h: ExtensibleHash):
    print("\n=== INSERÇÕES ===")
    for step, k in enumerate([1, 2, 3, 4, 5, 8, 12, 16, 20], start=1):
        print(f"\nInserindo chave {k}...")
        h.insert(k, f"valor_{k}")
        h.display()
        mostrar_tabela(h)
        visualizar_hash(h, step_name=f"insert_{step:02d}")
    print("\n-- Inserções concluídas --\n")


def demo_search(h: ExtensibleHash):
    print("\n=== BUSCAS ===")
    for k in [1, 4, 6, 10]:
        v = h.search(k)
        if v is not None:
            print(f"Chave {k} encontrada → {v}")
        else:
            print(f"Chave {k} não encontrada!")
    print("\n-- Buscas concluídas --\n")


def demo_remove(h: ExtensibleHash):
    print("\n=== REMOÇÕES ===")
    for step, k in enumerate([2, 5, 3, 7, 12], start=1):
        result = h.remove(k)
        msg = "Removido" if result else "Não encontrado"
        print(f"Chave {k}: {msg}")
        h.display()
        mostrar_tabela(h)
        visualizar_hash(h, step_name=f"remove_{step:02d}")
    print("\n-- Remoções concluídas --\n")


if __name__ == "__main__":
    print("==== Demonstração da Tabela Hash Extensível ====")
    h = ExtensibleHash(bucket_size=2)

    demo_insert(h)
    demo_search(h)
    demo_remove(h)

    print("==== Demonstração finalizada ====")
