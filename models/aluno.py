from typing import TypedDict

#Define a estrutura de um aluno, indicando que nome deve ser texto e idade um número inteiro.
class Aluno(TypedDict):
    nome: str
    idade: int