import pytest
from src.infrastructure.loaders.task_yaml_loader import TaskLoader
from crewai import Task


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
    t = TaskLoader.load_tasks(td)
    assert hasattr(t, "description")
