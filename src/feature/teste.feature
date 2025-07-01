Feature: Versionar Modalidade

  Scenario: Usuário solicita a listagem das modalidades de bolsa disponíveis
    Given o usuário está autenticado no sistema
    When ele acessa o endpoint de modalidades de bolsa
    Then o sistema retorna todas as modalidades de bolsa cadastradas