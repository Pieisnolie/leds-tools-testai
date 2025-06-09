from src.application.use_cases.crew_gherkin import crew_gherkin

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

if __name__ == "__main__":
    resultado = crew_gherkin("Listar modalidades de pagamento", strings)
    print(resultado)