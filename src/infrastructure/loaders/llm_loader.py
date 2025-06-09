import os
from crewai import LLM

class LLM_Loader:
    @staticmethod
    def load_from_params(
        model: str = None,
        temp: float = None,
        api_key: str = None
    ) -> LLM:
        """
        Carrega a entidade LLM a partir de parâmetros fornecidos ou das variáveis de ambiente.

        :param model: Nome do modelo LLM.
        :param temp: Temperatura para geração de texto.
        :param api_key: Chave de API para acessar o modelo.
        :return: Instância da entidade llm.
        """
        model = model or os.getenv("LLM_MODEL", "gemini/gemini-1.5-flash")
        temp = temp if temp is not None else float(os.getenv("LLM_TEMPERATURE", 0.0))
        api_key = api_key or os.getenv("GOOGLE_API_KEY")

        return LLM(
            model=model,
            temp=temp,
            api_key=api_key
        )