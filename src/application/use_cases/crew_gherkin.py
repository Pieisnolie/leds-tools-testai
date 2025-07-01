#import json
#import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from typing import Dict, List
from src.infrastructure.loaders.agent_loader import AgentLoader
from src.infrastructure.loaders.llm_loader import LLM_Loader
from src.infrastructure.loaders.task_yaml_loader import TaskLoader
from src.infrastructure.loaders.read_yaml import read_yaml_strings
import asyncio
import time

#
# DEBUG DA API:
#import litellm
#litellm._turn_on_debug()  # Ativa debug
#response = litellm.completion(
#     model=os.getenv("LLM_MODEL"),  # "gemini/gemini-1.5-flash"
#     messages=[{"role": "user", "content": "Olá, mundo!"}],
#     api_key=os.getenv("GEMINI_API_KEY")  # Chave corrigida
#)
#print(response)

load_dotenv() 

def crew_gherkin(user_case: str, strings: Dict[str, str]) -> str:
    
    llm_low_temp: LLM = LLM_Loader.load_from_params()
    llm_high_temp: LLM = LLM_Loader.load_from_params(temp=0.6)

    agents_dict: Dict[str, dict] = strings["agents"]
    tasks_dict: Dict[str, dict] = strings["tasks"]
    
    tasks: List[Task] = []
    agents: List[Agent] = []

    for turn in range(1, 4):
        writer_dict = agents_dict['gherkin_writer'].copy()
        writer_dict['role'] = writer_dict['role'].format(turn=turn)
        gherkin_writer_agent: Agent = AgentLoader.load_agents(writer_dict, llm_high_temp)

        reviewer_dict = agents_dict['gherkin_reviewer'].copy()
        reviewer_dict['role'] = reviewer_dict['role'].format(turn=turn)
        gherkin_reviewer_agent: Agent = AgentLoader.load_agents(reviewer_dict, llm_low_temp)

        code_task_dict = tasks_dict["gherkin_code"].copy()
        code_task_dict["description"] = code_task_dict["description"].format(user_case=user_case)
        task_gherkin_code: Task = TaskLoader.load_tasks(
            code_task_dict,
            gherkin_writer_agent,
            #output_file=f"etapas_geracao/rodada_{turn}.cs"
        )

        review_task_dict = tasks_dict["gherkin_review"].copy()
        review_task_dict["description"] = review_task_dict["description"].format(user_case=user_case)
        task_gherkin_review: Task = TaskLoader.load_tasks(
            review_task_dict,
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
        output_file="src/features/ListarModalidadeFeature.feature",
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

if __name__ == "__main__":
    with open("src/andes/test.andes") as file:
        andes = file.read()
        agents_dict, tasks_dict, outputs_dict = read_yaml_strings()
        strings = {"agents": agents_dict, "tasks": tasks_dict, "outputs": outputs_dict}
        #print(agents_dict)
        #print(tasks_dict.keys())
        #print(tasks_dict["gherkin_code"].keys())
        start_time = time.time()
        resultado = crew_gherkin(andes, strings)
        end_time = time.time()
        print(resultado)
        print(f"Tempo de execução: {end_time-start_time}")