#import json
#import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from crewai import Crew, Process
from typing import Dict, List
from src.infrastructure.loaders.agent_yaml_loader import AgentLoader
from src.infrastructure.loaders.llm_loader import LLM_Loader
from src.infrastructure.loaders.task_yaml_loader import TaskLoader
import os
from dotenv import load_dotenv

# DEBUG DA API:
# import litellm
# litellm._turn_on_debug()  # Ativa debug
# response = litellm.completion(
#     model=os.getenv("LLM_MODEL"),  # "gemini/gemini-1.5-flash"
#     messages=[{"role": "user", "content": "Olá, mundo!"}],
#     api_key=os.getenv("GEMINI_API_KEY")  # Chave corrigida
# )
# print(response)

load_dotenv() 

def crew_gherkin(user_case: str, strings: Dict[str, str]) -> str:
    
    llm_low_temp = LLM_Loader.load_from_params()
    llm_high_temp = LLM_Loader.load_from_params(temp=0.6)

    agents_dict: Dict[str, str] = strings["agents"]
    tasks_dict: Dict[str, str] = strings["tasks"]
    
    tasks: List[Task] = []
    agents: List[Agent] = []

    for turn in range(1,4):
        agents_dict['gherkin_writer']['role'] = agents_dict['gherkin_writer']['role'].format(turn=turn)
        gherkin_writer_agent: Agent = AgentLoader.load_agents(agents_dict["gherkin_writer"], llm_high_temp)

        agents_dict['gherkin_reviewer']['role'] = agents_dict['gherkin_reviewer']['role'].format(turn=turn)
        gherkin_reviewer_agent: Agent = AgentLoader.load_agents(agents_dict["gherkin_reviewer"], llm_low_temp)

        tasks_dict["gherkin_code"]["description"] = tasks_dict["gherkin_code"]["description"].format(user_case=user_case)
        task_gherkin_code: Task = TaskLoader.load_tasks(
            tasks_dict["gherkin_code"],
            gherkin_writer_agent,
            #output_file=f"etapas_geracao/rodada_{turn}.cs"
        )

        tasks_dict["gherkin_review"]["description"] = tasks_dict["gherkin_review"]["description"].format(user_case=user_case)
        task_gherkin_review: Task = TaskLoader.load_tasks(
            tasks_dict["gherkin_review"],
            gherkin_reviewer_agent,
            context=[task_gherkin_code],
            #output_file=f"etapas_geracao/revisao_{turn}.cs"
        )
        
        agents.append(gherkin_writer_agent)
        agents.append(gherkin_reviewer_agent)

        tasks.append(task_gherkin_code)
        tasks.append(task_gherkin_review)

    manager: Agent = AgentLoader.load_agents(agents_dict["manager_gherkin"], llm_low_temp)
    final_task: Task = TaskLoader.load_tasks(
        tasks_dict["manager_gherkin_task"],
        agent=manager,
        context=tasks[1::2],
        output_file="features/ListarModalidadeFeature.feature",
    )

    crew: Crew = Crew(
        agents=agents+[manager],
        tasks=tasks+[final_task],
        max_rpm=10,
        output_log_file="crew_log.txt",
        #manager_agent=manager_agent,
        manager_llm=llm_low_temp,
        process=Process.sequential,
        verbose=True
        
    )
    
    resultado = crew.kickoff()
    return resultado.raw