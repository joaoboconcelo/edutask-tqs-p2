"""Falha intencional temporaria para comprovar o bloqueio do CI."""
def test_pipeline_detecta_falha_controlada():
    assert False, "Demonstracao controlada: este teste deve falhar no Actions"
