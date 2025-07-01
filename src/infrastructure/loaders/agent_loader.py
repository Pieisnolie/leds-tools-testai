from crewai import Agent, LLM  

class AgentLoader():
    @staticmethod
    def load_agents(agent_dict: dict, llm: LLM) -> Agent:
        if not isinstance(llm, LLM):
            raise AttributeError("llm deve ser uma instância de LLM")
        return Agent(
            role=agent_dict["role"],
            goal=agent_dict["goal"],
            backstory=agent_dict["backstory"],
            llm=llm,
            config=None,
            cache=False,
            verbose=False,
            max_rpm=10,
            allow_delegation=False,
            tools=[],
            max_iter=100,
            function_calling_llm=None,
            max_execution_time=3600,
            step_callback=None,
            system_template="",
            prompt_template="",
            response_template="",
            allow_code_execution=False,
            max_retry_limit=3,
            use_system_prompt=True,
            respect_context_window=True,
            code_execution_mode="safe"
        )