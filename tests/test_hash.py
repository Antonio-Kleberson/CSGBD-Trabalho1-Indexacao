# tests/test_hash_merge.py
from src.extensible_hash.hash_extensible import ExtensibleHash

def test_merge_and_shrink():
    h = ExtensibleHash(bucket_size=2)
    # Inserir chaves que gerem splits e aumento de global_depth
    h.insert(0, "v0")
    h.insert(1, "v1")
    h.insert(2, "v2")
    h.insert(3, "v3")
    # Agora deve ter global_depth >= 2 (dependendo do hashing)
    assert h.search(0) == "v0"
    assert h.search(1) == "v1"
    assert h.search(2) == "v2"
    assert h.search(3) == "v3"

    # Remover chaves para forçar merges e possível shrink
    h.remove(3)
    h.remove(2)
    # Depois de remover 2 e 3, é provável que dois buckets se unam e global_depth reduza
    # Checar integridade das chaves restantes
    assert h.search(0) == "v0"
    assert h.search(1) == "v1"
    # global_depth deve ser pelo menos 1
    assert h.global_depth >= 1
