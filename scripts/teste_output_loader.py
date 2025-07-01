from infrastructure.loaders.output_example_yaml_loader import load_output_examples

def test_load_output_examples():
    """
    Testa a função load_output_examples para verificar se os exemplos de saída são carregados corretamente.
    """
    try:
        examples = load_output_examples()
        print("Exemplos carregados com sucesso:")
        for key, value in examples.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"Erro ao carregar os exemplos: {e}")

if __name__ == "__main__":
    test_load_output_examples()

# linha para rodar => python -m scripts.teste_output_loader