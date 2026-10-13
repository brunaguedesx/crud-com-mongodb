from pymongo import MongoClient

# Conecta ao MongoDB, consulta todos os alunos cadastrados na coleção "alunos" e exibe seus dados no terminal.
URI = "mongodb://localhost:27017"
client = MongoClient(URI)

try:
    database = client.get_database("meu_banco")
    alunos = database.get_collection("alunos")

    for aluno in alunos.find():
        print(aluno)

    client.close()
except Exception as e:
    raise Exception(f"Ocorreu um erro {e}")

