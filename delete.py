from pymongo import MongoClient

URI = "mongodb://localhost:27017"
client = MongoClient(URI)

try:
    database = client.get_database("meu_banco")
    alunos = database.get_collection("alunos")

    query = {"nome": "Fulano"}

    resultado = alunos.delete_one(query)

    print(f"Documentos deletados: {resultado.deleted_count}")

    client.close()
except Exception as e:
    raise Exception(f"Ocorreu um erro {e}")