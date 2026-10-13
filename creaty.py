from models.aluno import Aluno
from pymongo import MongoClient

# Conecta ao MongoDB e cadastra um novo aluno com nome e idade na coleção "alunos".
URI = "mongodb://localhost:27017"
client = MongoClient(URI)

try:
    database = client.get_database("meu_banco")
    alunos = database.get_collection("alunos")
    novo_aluno = Aluno(nome="Fulano", idade=30)
    alunos.insert_one(novo_aluno)

    client.close()
except Exception as e:
    raise Exception(f"Ocorreu um erro {e}")