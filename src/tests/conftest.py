import pytest

@pytest.fixture(scope="session")
def example_event():
    return {
        "evento": "Cadastrar nova modalidade de bolsa com todos os dados"
    }
