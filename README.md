# 🚀 TaskFlow API

> API REST profissional para gerenciamento de tarefas — FastAPI · PostgreSQL · JWT

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)

---

## ✨ Funcionalidades

- 🔐 Autenticação JWT (registro, login, rotas protegidas)
- 📋 CRUD completo de tarefas com status e prioridade
- 🗂️ Categorias personalizadas por usuário
- 🔎 Filtros por status, prioridade e categoria
- 📄 Paginação nos resultados
- ⏱️ Timestamps automáticos
- 🧠 Validações com Pydantic v2
- 🪵 Logs estruturados
- 🐳 Docker + Docker Compose prontos

---

## 🧱 Stack

| Camada        | Tecnologia              |
|---------------|-------------------------|
| Framework     | FastAPI 0.111           |
| Banco de dados| PostgreSQL 16           |
| ORM           | SQLAlchemy 2.0          |
| Auth          | python-jose (JWT)       |
| Senha         | passlib (bcrypt)        |
| Validação     | Pydantic v2             |
| Servidor      | Uvicorn                 |
| Container     | Docker + Compose        |

---

## 🗂️ Estrutura do Projeto

```
app/
├── main.py                  # Entry point, middlewares, rotas
├── core/
│   ├── config.py            # Configurações via .env
│   ├── security.py          # JWT, hash, dependência de auth
│   └── logging.py           # Setup de logs
├── database/
│   └── connection.py        # Engine, sessão, Base
├── models/
│   ├── user.py
│   ├── task.py
│   └── category.py
├── schemas/
│   ├── user.py
│   ├── task.py
│   └── category.py
├── services/
│   ├── user_service.py
│   ├── task_service.py
│   └── category_service.py
└── routes/
    ├── user_routes.py
    ├── task_routes.py
    └── category_routes.py
```

---

## ⚡ Como Rodar

### Opção 1 — Docker (recomendado)

```bash
git clone https://github.com/seu-usuario/taskflow-api.git
cd taskflow-api
cp .env.example .env
docker-compose up --build
```

API disponível em: `http://localhost:8000`
Swagger UI em: `http://localhost:8000/docs`

### Opção 2 — Local

```bash
# 1. Clone e entre no projeto
git clone https://github.com/seu-usuario/taskflow-api.git
cd taskflow-api

# 2. Crie e ative o virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com sua DATABASE_URL e SECRET_KEY

# 5. Suba o servidor
uvicorn app.main:app --reload
```

---

## 🌐 Endpoints

### 🔐 Auth

| Método | Rota            | Descrição                    | Auth? |
|--------|-----------------|------------------------------|-------|
| POST   | `/auth/register`| Cria conta e retorna JWT     | ❌    |
| POST   | `/auth/login`   | Login e retorna JWT          | ❌    |
| GET    | `/auth/me`      | Dados do usuário autenticado | ✅    |

### 📋 Tarefas

| Método | Rota              | Descrição                         | Auth? |
|--------|-------------------|-----------------------------------|-------|
| GET    | `/tasks`          | Lista tarefas (filtros + paginação)| ✅   |
| POST   | `/tasks`          | Cria uma tarefa                   | ✅    |
| GET    | `/tasks/{id}`     | Detalhe de uma tarefa             | ✅    |
| PUT    | `/tasks/{id}`     | Atualiza uma tarefa               | ✅    |
| DELETE | `/tasks/{id}`     | Remove uma tarefa                 | ✅    |

**Query params disponíveis em `GET /tasks`:**
- `status` → `pending` | `in_progress` | `done`
- `priority` → `low` | `medium` | `high`
- `category_id` → ID numérico
- `page` → padrão: 1
- `per_page` → padrão: 10, máx: 100

### 🗂️ Categorias

| Método | Rota                  | Descrição           | Auth? |
|--------|-----------------------|---------------------|-------|
| GET    | `/categories`         | Lista categorias    | ✅    |
| POST   | `/categories`         | Cria categoria      | ✅    |
| DELETE | `/categories/{id}`    | Remove categoria    | ✅    |

---

## 🔐 Autenticação

Todas as rotas protegidas exigem o header:

```
Authorization: Bearer <seu_token_jwt>
```

O token é retornado ao fazer `/auth/register` ou `/auth/login`.

---

## 📦 Variáveis de Ambiente

```env
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow_db
SECRET_KEY=sua-chave-secreta-super-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 🚀 Deploy

### Render

1. Crie um novo **Web Service** apontando para este repositório
2. Build Command: `pip install -r requirements.txt`
3. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Adicione as variáveis de ambiente no painel

### Railway

```bash
railway login
railway init
railway up
```

---

## 📄 Licença

MIT © 2025