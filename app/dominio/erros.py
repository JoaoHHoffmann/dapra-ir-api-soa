class RegraViolada(ValueError):
    """Uma regra do domínio foi quebrada (vira HTTP 422 na API)."""