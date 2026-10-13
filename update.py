from pymongo import MongoClient

# Conecta ao MongoDB e atualiza o nome e a idade de um aluno específico na coleção "alunos".
URI = "mongodb://localhost:27017"
client = MongoClient(URI)

try:
    database = client.get_database("meu_banco")
    alunos = database.get_collection("alunos")

    query = {"_id": "xxx"}  
    operation = {"$set": {"nome": "Newton", "idade": 45}}
    alunos.update_one(query, operation)

    client.close()
except Exception as e:
    raise Exception(f"Ocorreu um erro {e}")