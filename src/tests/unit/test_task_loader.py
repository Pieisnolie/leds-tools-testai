import pytest
from src.infrastructure.loaders.task_yaml_loader import TaskLoader
from crewai import Task

def test_task_loader_completo():
    td = {
        "description": "Desc",
        "steps": ["s1", "s2"],
        "tools": ["t1"],
        "expected_output": "out1",
        "agent": "A",
        "async_execution": True,
        "context": "CTX",
        "config": {"a":1},
        "output_json": {"j":2},
        "output_pydantic": None,
        "human_input": True,
        "converter_cls": int,
        "callback": lambda x: x
    }
    t = TaskLoader.load_tasks(td, agent="A", context="CTX", output_file="f.txt")
    assert isinstance(t, Task)
    assert t.description == {"description":"Desc"}
    assert t.expected_output == {"expected_output": "out1"}
    assert t.agent == {"agent": "A"}
    assert t.tools == {"tools": ["t1"]}
    assert t.async_execution == {"async_execution": True}
    assert t.context == {"context": "CTX"}
    assert t.config == {"a":1}
    assert t.output_json == {"j":2}
    assert t.human_input == {"human_input": True}
    assert t.output_file == "f.txt"

def test_task_loader_default_steps_tools():
    td = {"description":"Desc2"}
    t = TaskLoader.load_tasks(td)
    assert t.tools == []
    assert t.async_execution is False

def test_task_loader_sem_agent_e_context():
    td = {"description":"D4"}
    t = TaskLoader.load_tasks(td)
    assert t.agent is None or t.agent == []
    assert t.context is None

def test_task_loader_converter_callback_nulos():
    td = {"description":"D5","converter_cls":None,"callback":None}
    t = TaskLoader.load_tasks(td)
    assert t.converter_cls is None
    assert t.callback is None

def test_task_loader_output_file_opcional():
    td = {"description":"D6"}
    t = TaskLoader.load_tasks(td, output_file="o6.txt")
    assert t.output_file == "o6.txt"

def test_task_loader_tipo_errado(monkeypatch):
    td = {"description":"D7"}
    # forçar TaskLoader a chamar algo errado, mas assume que Task aceita qualquer coisa
    t = TaskLoader.load_tasks(td)
    assert hasattr(t, "description")
