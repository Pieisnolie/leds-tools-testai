import pytest
from src.infrastructure.loaders.task_loader import TaskLoader
from src.domain.entities.task import Task

@pytest.fixture
def tasks_dict_mock():
    return {
        "task1": {
            "description": "Generate Gherkin code",
            "expected_output": "Only Gherkin"
        },
        "task2": {
            "description": "Review the generated code",
            "expected_output": "Corrected Gherkin"
        }
    }

def test_load_tasks(tasks_dict_mock):
    loader = TaskLoader()
    tasks = loader.load_tasks(tasks_dict_mock)

    assert len(tasks) == 2
    assert isinstance(tasks[0], Task)
    assert "Generate Gherkin" in str(tasks[0].description)
    assert "Corrected Gherkin" in str(tasks[1].expected_output)
