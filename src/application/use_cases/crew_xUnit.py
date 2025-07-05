from crewai import Process, LLM, Task, Agent, Crew
from crewai_tools import FileReadTool, DirectoryReadTool
from typing import Dict, List
from src.infrastructure.loaders.task_yaml_loader import TaskLoader
from src.infrastructure.loaders.agent_loader import AgentLoader
from src.infrastructure.loaders.llm_loader import LLM_Loader
from src.infrastructure.loaders.read_yaml import read_yaml_strings
from dotenv import load_dotenv
import asyncio
import time
import os

load_dotenv()
# Definem os diretórios dinâmicos
REPO_ROOT = os.getcwd()  # Onde o usuário está (raiz do projeto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

# Caminhos adaptados dinamicamente
dtos_path = os.path.join(REPO_ROOT, "dtos")
end_points_path = os.path.join(REPO_ROOT, "docs", "endpoints.txt")


agents_dict, tasks_dict, outputs_dict = read_yaml_strings()

llm_high_temp: LLM = LLM_Loader.load_from_params(temp=0.8)
llm_low_temp: LLM = LLM_Loader.load_from_params()

def crew_xunit_debate(feature: str, strings: Dict[str, str]) -> str:
    agents_dict = strings["agents"]
    tasks_dict = strings["tasks"]

    tasks: List[Task] = []
    agents: List[Agent] = []

    gemini_llm: LLM = LLM_Loader.load_from_params(temp=0.2)

    csharp_xunit_writer_agent: Agent = AgentLoader.load_agents(agents_dict["csharp_xunit_writer"], gemini_llm)

    xunit_code_proposal_dict = tasks_dict["xunit_code_proposal"].copy()
    xunit_code_proposal_dict["description"] = xunit_code_proposal_dict["description"].format(feature=feature)
    xunit_code_proposal: Task = TaskLoader.load_tasks(xunit_code_proposal_dict, agent=csharp_xunit_writer_agent)

    agents.append(csharp_xunit_writer_agent)
    tasks.append(xunit_code_proposal)

    for i in range(1, 4):
        xunit_solution_discussion_agent: Agent = AgentLoader.load_agents(agents_dict["xunit_solution_discussion"], gemini_llm)

        debate_dict = tasks_dict["debate"].copy()
        debate_dict["description"] = debate_dict["description"].format(feature=feature)
        debate: Task = TaskLoader.load_tasks(debate_dict, agent=xunit_solution_discussion_agent)

        agents.append(xunit_solution_discussion_agent)
        tasks.append(debate)

    result_analysis_manager_agent: Agent = AgentLoader.load_agents(agents_dict["result_analysis_manager"], gemini_llm)

    manager_xunit_task_dict = tasks_dict["manager_xunit_task"].copy()
    manager_xunit_task_dict["description"] = manager_xunit_task_dict["description"].format(feature=feature)
    manager_xunit_task: Task = TaskLoader.load_tasks(
        manager_xunit_task_dict,
        output_file=f"modalidade_bolsa_crew.cs",
        agent=result_analysis_manager_agent,
        context=[tasks[-1]],
    )

    crew: Crew = Crew(
        agents=agents + [result_analysis_manager_agent],
        tasks=tasks + [manager_xunit_task],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff().raw

def info_gatherer_crew(feature: str) -> tuple[str, str]:
    agent_api_finder = Agent(
        role="API Path Finder",
        goal="Identify and extract API URL paths from Swagger documents to streamline API integration and documentation.",
        backstory="A meticulous and detail-oriented digital assistant, trained extensively in API documentation and Swagger standards. Equipped with a keen eye for structure and patterns, the agent thrives in simplifying complex API schemas for developers.",
        llm=llm_low_temp,
        verbose=True,
        tools=[FileReadTool()],
    )

    agent_file_searcher = Agent(
        role="File Search Specialist",
        goal="Locate a specific file within a given directory and its subdirectories, ensuring efficient file retrieval for various tasks.",
        backstory="A diligent and organized assistant, fine-tuned for file system navigation and pattern matching. With a background in file management and search optimization, this agent excels at quickly identifying files based on name, type, or content.",
        llm=llm_low_temp,
        tools=[DirectoryReadTool(), FileReadTool()]
    )

    dto_file_find = Task(
        description=f"{feature}\nAt the path {dtos_path}\nFind the dto request file and response file for the given feature,\nthe open the file and read it content\n",
        expected_output="The dto response and request class code",
        agent=agent_file_searcher,
        async_execution=True
    )

    api_url_find = Task(
        description=f"{feature}\nRead the file at {end_points_path}\nUse the tool to search for the api url for the given Feature;\nThe api_url has the feature title all in lower case;\nYou should look not only for the exact correspondence, but also for similars. For example, if the feature title in lowercase is versaomodalidade, you should also consider versaomodalidadebolsa\n",
        expected_output="Only the complete url path requested and the respective methods",
        agent=agent_api_finder,
    )

    crew = Crew(
        agents=[agent_api_finder, agent_file_searcher],
        tasks=[dto_file_find, api_url_find],
        verbose=True,
        process=Process.sequential
    )

    crew.kickoff()

    print(api_url_find.output.raw, file=open("api_url.txt", "w"))
    print(dto_file_find.output.raw, file=open("dto_code.txt", "w"))

    return dto_file_find.output.raw, api_url_find.output.raw

def crew_xunit_generation(feature: str, api_url, dto_code) -> Crew:
    gemini_llm: LLM = LLM_Loader.load_from_params(temp=0.2)
    agents: list[Agent] = []
    tasks: list[Task] = []

    xunit_code_proposal_dict = tasks_dict["xunit_code_proposal"].copy()
    xunit_code_proposal_dict["description"] = (
        xunit_code_proposal_dict["description"].format(feature=feature)
        + "The DTO class you should use is: " + dto_code + "\n"
        + "The url for this feature is " + api_url + "\n"
        + outputs_dict[xunit_code_proposal_dict["output_example"]]
    )
    print(xunit_code_proposal_dict["description"], file=open("xunit_code_proposal_desc.txt", "w"))

    xunit_review_dict = tasks_dict["xunit_review"].copy()
    xunit_review_dict["description"] = (
        xunit_review_dict["description"].format(feature=feature)
        + outputs_dict[xunit_review_dict["output_example"]]
    )

    csharp_xunit_writer_agent: Agent = AgentLoader.load_agents(agents_dict["csharp_xunit_writer"], gemini_llm)
    xunit_code_proposal: Task = TaskLoader.load_tasks(
        xunit_code_proposal_dict,
        agent=csharp_xunit_writer_agent,
    )

    agents.append(csharp_xunit_writer_agent)    
    tasks.append(xunit_code_proposal)

    xunit_code_reviewer_agent: Agent = AgentLoader.load_agents(agents_dict["xunit_code_reviewer_agent"], gemini_llm)
    xunit_code_review_task: Task = TaskLoader.load_tasks(
        xunit_review_dict,
        xunit_code_reviewer_agent,
        context=[xunit_code_proposal],
    )

    agents.append(xunit_code_reviewer_agent)
    tasks.append(xunit_code_review_task)

    return Crew(
        agents=agents,
        tasks=tasks,
        max_rpm=10,
        output_log_file="crew_log.txt",
        manager_llm=llm_low_temp,
        process=Process.sequential,
        verbose=True
    )

def manager_crew(reviews: tuple[str]) -> None:
    manager_xunit_task_dict = tasks_dict["manager_xunit_task"].copy()
    manager_xunit_task_dict["description"] = (
        manager_xunit_task_dict["description"].format(reviews[0], reviews[1], reviews[2])
        + outputs_dict[manager_xunit_task_dict["output_example"]]
    )
    print(manager_xunit_task_dict["description"], file=open("manager_xunit_task_desc.txt", "w"))

    manager: Agent = AgentLoader.load_agents(agents_dict["result_analysis_manager"], llm_low_temp)
    manager_task: Task = TaskLoader.load_tasks(
        manager_xunit_task_dict,
        manager,
        output_file="resposta/VersionarModalidadeStepAI.cs"
    )

    crew = Crew(
        agents=[manager],
        tasks=[manager_task],
        process=Process.sequential
    )

    return crew.kickoff()

async def xunit_generation(feature):
    dto_code, api_url = info_gatherer_crew(feature)
    crew_xunit: Crew = crew_xunit_generation(feature, api_url, dto_code)
    result1 = crew_xunit.kickoff_async()
    result2 = crew_xunit.kickoff_async()
    result3 = crew_xunit.kickoff_async()

    results = await asyncio.gather(result1, result2, result3)
    return manager_crew(results)

if __name__ == "__main__":
    file = input("Digite o nome do arquivo FEATURE (sem extensão): ")
    with open(f"features/{file}.feature") as file:
        feature = file.read()
        start_time = time.time()
        asyncio.run(xunit_generation(feature))
        end_time = time.time()
        print(f"Tempo de execução: {end_time-start_time}")