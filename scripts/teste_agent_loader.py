from src.domain.entities.llm import llm
from src.infrastructure.loaders.agent_yaml_loader import AgentLoader
from src.infrastructure.loaders.llm_loader import LLM_Loader 
from typing import Dict, List

def main():

    llm_high_temp: llm = LLM_Loader.load_from_params(temperature=0.6)
    # Dicionário com os dados dos agentes
    strings = {
        "agents": {
            "gherkin_writer": {
                "role": "Writer {turn}",
                "goal": "Escrever cenários",
                "backstory": "Especialista em Gherkin"
            },
            "gherkin_reviewer": {
                "role": "Reviewer {turn}",
                "goal": "Revisar cenários",
                "backstory": "Especialista em revisão"
            },
            "manager_gherkin": {
                "role": "Manager",
                "goal": "Gerenciar",
                "backstory": "Gerente"
            }
        },
        "tasks": {
            "gherkin_code": {
                "description": "Gerar código para {user_case}"
            },
            "gherkin_review": {
                "description": "Revisar código para {user_case}"
            },
            "manager_gherkin_task": {
                "description": "Finalizar para {user_case}"
            }
        }
    }
    agents_dict: Dict[str, str] = strings["agents"]

    # Cria uma instância do loader
    loader = AgentLoader()

    # Carrega os agentes a partir do dicionário
    agents = loader.load_agents(agents_dict["gherkin_writer"], llm_high_temp)  # Substitua 'llm=None' pelo seu LLM se necessário

    # Exibe os agentes carregados
    for agent in agents:
        print(agent)

if __name__ == "__main__":
    main()


## linha pra rodar => python -m scripts.teste_agent_loader