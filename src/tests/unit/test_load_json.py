import json
import pytest
from src.infrastructure.loaders.data_loader import load_json

def test_load_json_valido(tmp_path):
    dados = {"a":1}
    p = tmp_path / "x.json"
    p.write_text(json.dumps(dados), encoding="utf-8")
    assert load_json(str(p)) == dados

def test_load_json_nao_encontra(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_json("inexistente.json")

def test_load_json_arquivo_vazio(tmp_path):
    p = tmp_path / "vazio.json"
    p.write_text("", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json(str(p))

def test_load_json_conteudo_invalido(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{no: json}", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_json(str(p))

def test_load_json_unicode(tmp_path):
    dados = {"ç": "áé"}
    p = tmp_path / "uni.json"
    p.write_text(json.dumps(dados), encoding="utf-8")
    assert load_json(str(p)) == dados

def test_load_json_grande(tmp_path):
    dados = list(range(1000))
    p = tmp_path / "big.json"
    p.write_text(json.dumps(dados), encoding="utf-8")
    assert load_json(str(p)) == dados

def test_load_json_permissao_negada(tmp_path, monkeypatch):
    p = tmp_path / "x.json"
    p.write_text("{}", encoding="utf-8")
    def fake_open(*args, **kwargs):
        raise PermissionError()
    monkeypatch.setattr("builtins.open", fake_open)
    with pytest.raises(PermissionError):
        load_json(str(p))

def test_load_json_caminho_diretorio(tmp_path):
    with pytest.raises(PermissionError):
        load_json(str(tmp_path))
