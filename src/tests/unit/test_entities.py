import pytest
from src.domain.entities.agent import Agent
from src.domain.entities.llm import llm
from src.domain.entities.task import Task

def test_llm_repr():
    model = llm(model="gpt-4", temperature=0.0, api_key="secret")
    assert "gpt-4" in repr(model)

def test_agent_repr():
    model = llm("gpt-4", 0.0, "secret")
    agent = Agent(
        name="TestAgent", role="Tester", goal="Break things", backstory="Born to test",
        llm=model, config=None, cache=False, verbose=False, max_rpm=10,
        allow_delegation=False, tools=[], max_iter=10, function_calling_llm=None,
        max_execution_time=1000, step_callback=None, system_template="",
        prompt_template="", response_template="", allow_code_execution=False,
        max_retry_limit=3, use_system_prompt=True, respect_context_window=True,
        code_execution_mode="safe"
    )
    assert "TestAgent" in repr(agent)

def test_task_repr():
    task = Task(
        name="TestTask",
        steps=["Step1", "Step2"],
        task_profile=["Description", "Expected Output"],
        agent=["AgentA"],
        tools=[],
        async_execution=False,
        context=None,
        config=None,
        output_json=None,
        output_pydantic=None,
        output_file=None,
        human_input=False,
        converter_cls=None,
        callback=None
    )
    assert "TestTask" in repr(task)
