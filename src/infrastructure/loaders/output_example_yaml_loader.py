import yaml
from typing import Dict

def load_output_examples(file_path: str = "src/config/output_examples.yaml") -> Dict[str, str]:
    """
    Carrega os exemplos de saída do arquivo YAML.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            output_examples = yaml.safe_load(file)
        return output_examples
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permissão negada ao abrir o arquivo: {file_path}")
    except yaml.YAMLError as e:
        raise ValueError(f"Erro ao carregar o arquivo YAML: {e}")