# src/extensible_hash/demo_hash.py
from .hash_extensible import ExtensibleHash
from graphviz import Digraph
import os


def visualizar_hash(hash_table, step_name="hash_step"):
    """Gera uma imagem da estrutura atual da tabela hash usando Graphviz."""
    dot = Digraph(comment=f"Extensible Hash - {step_name}")
    dot.attr(rankdir='LR', size='8,5')

    seen = {}
    # Cria nós para cada bucket
    for i, b in enumerate(hash_table.directory):
        dir_label = f"dir[{i:0{hash_table.global_depth}b}]"
        dot.node(dir_label, dir_label, shape="ellipse", color="black")

        # Se o bucket ainda não foi desenhado, adiciona
        if id(b) not in seen:
            seen[id(b)] = f"B{len(seen)}"
            bucket_label = seen[id(b)]
            conteudo = "\\n".join([f"{k}:{v}" for k, v in b.items]) or "(vazio)"
            dot.node(bucket_label,
                    f"{bucket_label}\\nld={b.local_depth}\\n{conteudo}",
                    shape="box", style="filled", color="lightblue")

        # Conecta diretório → bucket
        dot.edge(dir_label, seen[id(b)])

    # Garante que a pasta 'docs/prints' existe
    os.makedirs("docs/prints", exist_ok=True)
    output_path = f"docs/prints/{step_name}"
    dot.render(output_path, format="png", cleanup=True)
    print(f" Diagrama gerado: {output_path}.pdf")


def demo_insert(h: ExtensibleHash):
    print("\n=== INSERÇÕES ===")
    for step, k in enumerate([1, 2, 3, 4, 5, 6, 22, 10, 14], start=1):
        print(f"\nInserindo chave {k}...")
        h.insert(k, f"valor_{k}")
        h.display()
        visualizar_hash(h, step_name=f"insert_{step:02d}")
    print("\n-- Inserções concluídas --\n")


def demo_search(h: ExtensibleHash):
    print("\n=== BUSCAS ===")
    for k in [1, 4, 6, 10, 12]:
        v = h.search(k)
        if v is not None:
            print(f"Chave {k} encontrada → {v}")
        else:
            print(f"Chave {k} não encontrada!")
    print("\n-- Buscas concluídas --\n")


def demo_remove(h: ExtensibleHash):
    print("\n=== REMOÇÕES ===")
    for step, k in enumerate([2, 5, 10, 13], start=1):
        result = h.remove(k)
        msg = "Removido" if result else "Não encontrado"
        print(f"Chave {k}: {msg}")
        h.display()
        visualizar_hash(h, step_name=f"remove_{step:02d}")
    print("\n-- Remoções concluídas --\n")


if __name__ == "__main__":
    print("==== Demonstração da Tabela Hash Extensível ====")
    h = ExtensibleHash(bucket_size=2)

    demo_insert(h)
    demo_search(h)
    demo_remove(h)

    print("==== Demonstração finalizada ====")
