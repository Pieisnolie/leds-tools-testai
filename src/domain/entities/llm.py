class llm:
    def __init__(self, model: str, temp: float, api_key: str):
        self.model = model
        self.temp = temp
        self.api_key = api_key

    def __repr__(self):
        return f"LLM(model={self.model}, temp={self.temp}, api_key={self.api_key})"