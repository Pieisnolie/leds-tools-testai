import requests

def test_api_gherkin_response():
    payload = {
        "evento": "Cadastrar uma nova modalidade de bolsa com dados obrigatórios"
    }

    response = requests.post("http://localhost:8000/gherkin", json=payload)

    assert response.status_code == 200
    assert "Scenario" in response.text
    assert "Given" in response.text or "Then" in response.text
