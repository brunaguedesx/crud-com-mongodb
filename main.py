from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from pymongo import MongoClient

# 1. Inicializa a aplicação FastAPI
app = FastAPI(
    title="API CRUD de Alunos",
    description="API integrada ao MongoDB usando PyMongo",
    version="1.0.0",
)

# 2. Conexão com o MongoDB no Docker
URI = "mongodb://localhost:27017"
client = MongoClient(URI)
database = client.get_database("meu_banco")
collection = database.get_collection("alunos")

# 3. Esquema de validação com Pydantic
class AlunoSchema(BaseModel):
    nome: str = Field(..., examples=["João"])
    idade: int = Field(..., gt=0, examples=[25])

# Função auxiliar para converter o ID do MongoDB em texto
def aluno_helper(aluno) -> dict:
    return {
        "id": str(aluno["_id"]),
        "nome": aluno["nome"],
        "idade": aluno["idade"],
    }

# --- ENDPOINTS / ROTAS DA API ---

# CRIAR (POST) - Insere um novo aluno
@app.post(
    "/alunos",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo aluno",
)
def criar_aluno(aluno: AlunoSchema):
    try:
        novo_aluno = aluno.model_dump()
        resultado = collection.insert_one(novo_aluno)
        doc_criado = collection.find_one({"_id": resultado.inserted_id})
        return aluno_helper(doc_criado)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# CONSULTAR TODOS (GET) - Lista todos os alunos
@app.get(
    "/alunos",
    status_code=status.HTTP_200_OK,
    summary="Listar todos os alunos",
)
def listar_alunos():
    try:
        return [aluno_helper(a) for a in collection.find()]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# CONSULTAR POR ID (GET) - Busca um aluno específico pelo ID
@app.get(
    "/alunos/{aluno_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar aluno por ID",
)
def buscar_aluno_por_id(aluno_id: str):
    try:
        obj_id = ObjectId(aluno_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID no formato inválido"
        )

    aluno = collection.find_one({"_id": obj_id})
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return aluno_helper(aluno)

# ATUALIZAR (PUT) - Atualiza os dados de um aluno
@app.put(
    "/alunos/{aluno_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar aluno por ID",
)
def atualizar_aluno(aluno_id: str, aluno: AlunoSchema):
    try:
        obj_id = ObjectId(aluno_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID no formato inválido"
        )

    resultado = collection.update_one(
        {"_id": obj_id}, {"$set": aluno.model_dump()}
    )
    if resultado.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return aluno_helper(collection.find_one({"_id": obj_id}))

# EXCLUIR (DELETE) - Remove um aluno pelo ID
@app.delete(
    "/alunos/{aluno_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover aluno por ID",
)
def deletar_aluno(aluno_id: str):
    try:
        obj_id = ObjectId(aluno_id)
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID no formato inválido"
        )

    resultado = collection.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )

    return {"mensagem": "Aluno removido com sucesso"}
