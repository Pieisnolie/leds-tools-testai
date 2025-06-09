import pytest
from src.infrastructure.loaders.agent_loader import AgentLoader
from src.domain.entities.agent import Agent

@pytest.fixture
def agents_dict_mock():
    return {
        "agent1": {
            "role": "Developer",
            "goal": "Write quality code",
            "backstory": "Experienced software engineer"
        },
        "agent2": {
            "role": "Reviewer",
            "goal": "Review Gherkin scenarios",
            "backstory": "Expert in BDD and testing"
        }
    }

def test_load_agents(agents_dict_mock):
    loader = AgentLoader()
    agents = loader.load_agents(agents_dict_mock)

    assert len(agents) == 2
    assert isinstance(agents[0], Agent)
    assert agents[0].role == "Developer"
    assert agents[1].goal == "Review Gherkin scenarios"
