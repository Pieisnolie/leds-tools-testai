import pytest
import yaml
from src.infrastructure.loaders.read_yaml import read_yaml_strings

def test_leitura_completa(tmp_path, monkeypatch):
    base = tmp_path / "src" / "config"
    base.mkdir(parents=True)
    (base / "agents.yaml").write_text(yaml.safe_dump({"a":1}), encoding="utf-8")
    (base / "tasks.yaml").write_text(yaml.safe_dump({"b":2}), encoding="utf-8")
    (base / "output_examples.yaml").write_text(yaml.safe_dump({"c":3}), encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    ag, ta, oe = read_yaml_strings()
    assert ag == {"a":1}
    assert ta == {"b":2}
    assert oe == {"c":3}

def test_falta_agents(monkeypatch, tmp_path):
    base = tmp_path / "src" / "config"
    base.mkdir(parents=True)
    (base / "tasks.yaml").write_text("{}", encoding="utf-8")
    (base / "output_examples.yaml").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        read_yaml_strings()

def test_falta_tasks(monkeypatch, tmp_path):
    base = tmp_path / "src" / "config"
    base.mkdir(parents=True)
    (base / "agents.yaml").write_text("{}", encoding="utf-8")
    (base / "output_examples.yaml").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        read_yaml_strings()

def test_falta_output_examples(monkeypatch, tmp_path):
    base = tmp_path / "src" / "config"
    base.mkdir(parents=True)
    (base / "agents.yaml").write_text("{}", encoding="utf-8")
    (base / "tasks.yaml").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        read_yaml_strings()


def test_preserva_ponteiro_de_cwd(tmp_path, monkeypatch):
    # garante que cwd não é alterado permanentemente
    base = tmp_path / "src" / "config"
    base.mkdir(parents=True)
    (base / "agents.yaml").write_text("{}", encoding="utf-8")
    (base / "tasks.yaml").write_text("{}", encoding="utf-8")
    (base / "output_examples.yaml").write_text("{}", encoding="utf-8")
    cwd_original = str(tmp_path)
    monkeypatch.chdir(tmp_path)
    read_yaml_strings()
    assert str(tmp_path) == cwd_original
