# ============================================================
#  API de To-Do com FastAPI
#  Para rodar:
#    1. pip install fastapi uvicorn
#    2. uvicorn main:app --reload
#    3. Acesse http://localhost:8000/docs para testar visualmente
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Criando a aplicação ---
app = FastAPI(
    title="Minha API de To-Do",
    description="API simples para gerenciar tarefas",
    version="1.0.0"
)

# ============================================================
# BANCO DE DADOS SIMULADO
# Por enquanto usamos uma lista em memória.
# Quando você evoluir, pode trocar por um banco real (SQLite, PostgreSQL etc.)
# ============================================================
tarefas = []
proximo_id = 1  # Contador para gerar IDs únicos


# ============================================================
# MODELOS (schemas)
# Pydantic valida automaticamente os dados que chegam na API
# ============================================================

class TarefaEntrada(BaseModel):
    """Dados que o usuário envia para criar/atualizar uma tarefa."""
    titulo: str
    descricao: Optional[str] = None  # campo opcional
    concluida: bool = False           # False por padrão


class Tarefa(TarefaEntrada):
    """Tarefa completa, com os campos gerados pelo servidor."""
    id: int
    criada_em: str


# ============================================================
# ROTAS (endpoints)
# Cada função abaixo é uma rota da API
# ============================================================

# --- GET / → Página inicial (só pra confirmar que a API tá viva) ---
@app.get("/")
def raiz():
    return {"mensagem": "API de To-Do funcionando! Acesse /docs para explorar."}


# --- GET /tarefas → Lista todas as tarefas ---
@app.get("/tarefas", response_model=list[Tarefa])
def listar_tarefas():
    return tarefas


# --- GET /tarefas/{id} → Busca uma tarefa pelo ID ---
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def buscar_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa
    # Se não encontrou, retorna erro 404
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# --- POST /tarefas → Cria uma nova tarefa ---
@app.post("/tarefas", response_model=Tarefa, status_code=201)
def criar_tarefa(dados: TarefaEntrada):
    global proximo_id

    nova_tarefa = {
        "id": proximo_id,
        "titulo": dados.titulo,
        "descricao": dados.descricao,
        "concluida": dados.concluida,
        "criada_em": datetime.now().strftime("%d/%m/%Y %H:%M")
    }

    tarefas.append(nova_tarefa)
    proximo_id += 1

    return nova_tarefa


# --- PUT /tarefas/{id} → Atualiza uma tarefa existente ---
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def atualizar_tarefa(tarefa_id: int, dados: TarefaEntrada):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["titulo"] = dados.titulo
            tarefa["descricao"] = dados.descricao
            tarefa["concluida"] = dados.concluida
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# --- DELETE /tarefas/{id} → Remove uma tarefa ---
@app.delete("/tarefas/{tarefa_id}")
def deletar_tarefa(tarefa_id: int):
    for i, tarefa in enumerate(tarefas):
        if tarefa["id"] == tarefa_id:
            tarefas.pop(i)
            return {"mensagem": f"Tarefa {tarefa_id} deletada com sucesso"}
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")


# --- PATCH /tarefas/{id}/concluir → Atalho para marcar como concluída ---
@app.patch("/tarefas/{tarefa_id}/concluir", response_model=Tarefa)
def concluir_tarefa(tarefa_id: int):
    for tarefa in tarefas:
        if tarefa["id"] == tarefa_id:
            tarefa["concluida"] = True
            return tarefa
    raise HTTPException(status_code=404, detail="Tarefa não encontrada")
