"""Valida a estrutura da entrada JSON antes de acessar campos ou persistência."""


def json_payload_error(payload, *, credentials=False):
    """Retorna uma mensagem de erro de contrato, ou None para entrada compatível."""
    if not isinstance(payload, dict):
        return "O corpo JSON deve ser um objeto."
    if credentials and any(
        not isinstance(payload.get(field, ""), str) for field in ("email", "password")
    ):
        return "E-mail e senha devem ser textos."
    return None
