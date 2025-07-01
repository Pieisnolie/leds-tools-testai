import pytest
import yaml
from src.infrastructure.loaders.output_example_yaml_loader import load_output_examples

def test_carrega_exemplos_validos(tmp_path):
    data = {"x": "y"}
    f = tmp_path / "o.yaml"
    f.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert load_output_examples(str(f)) == data

def test_arquivo_nao_encontrado():
    with pytest.raises(FileNotFoundError):
        load_output_examples("nao_existe.yaml")

def test_yaml_invalido(tmp_path):
    f = tmp_path / "bad.yaml"
    f.write_text("!!!", encoding="utf-8")
    with pytest.raises(ValueError):
        load_output_examples(str(f))

def test_retorna_none_para_yaml_vazio(tmp_path):
    f = tmp_path / "empty.yaml"
    f.write_text("", encoding="utf-8")
    assert load_output_examples(str(f)) is None

def test_carrega_estrutura_aninhada(tmp_path):
    data = {"a": {"b": 2}}
    f = tmp_path / "nested.yaml"
    f.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert load_output_examples(str(f)) == data

def test_permissao_negada(monkeypatch):
    def fake_open(*args, **kwargs):
        raise PermissionError("Permissão negada ao abrir o arquivo")
    monkeypatch.setattr("builtins.open", fake_open)
    with pytest.raises(PermissionError):
        load_output_examples("qualquer_arquivo.yaml")

def test_caminho_none():
    with pytest.raises(TypeError):
        load_output_examples(None)

def test_carrega_valores_numericos(tmp_path):
    data = {"num": 123}
    f = tmp_path / "num.yaml"
    f.write_text(yaml.safe_dump(data), encoding="utf-8")
    assert load_output_examples(str(f)) == data
