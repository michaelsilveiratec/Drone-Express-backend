# Orientador do Projeto: Professor Giovani Bontempo


# 🚁 DroneExpress - API de Gerenciamento de Entregas

Sistema web completo para registro, acompanhamento e gerenciamento de entregas realizadas por drones, com controle de qualidade, rastreamento em tempo real e relatórios operacionais.

## 📋 Sobre o Projeto

### Descrição
O **DroneExpress** é uma API RESTful desenvolvida para gerenciar o ciclo completo de entregas via drones. O sistema permite:

- ✅ Cadastro e gestão de consumidores
- ✅ Registro de empresas transportadoras
- ✅ Criação e acompanhamento de entregas
- ✅ Gerenciamento de produtos com categorização
- ✅ Validações de integridade referencial
- ✅ Testes automatizados completos

### Funcionalidades Principais
- **CRUD Completo** para todos os recursos (Consumidores, Empresas, Entregas, Produtos)
- **Validações** de email, CNPJ e integridade referencial
- **Operações PATCH** para atualizações parciais
- **Testes Automatizados** com 44 testes cobrindo todos endpoints
- **API Documentada** com Swagger UI
- **Banco de Dados Relacional** com SQLAlchemy ORM

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+** (testado em 3.14)
- **pip** (gerenciador de pacotes)
- **Git** (para clonar o repositório)

Verificar instalação:
```bash
python --version
pip --version
```

---

## 🚀 Instalação Rápida

### Passo 1: Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd ap1-backend-fastapi-grupo-fgcmj
```

### Passo 2: Instale as dependências
```bash
pip install -r requirements.txt
```

### Passo 3: Crie o banco de dados
```bash
python -m fast_zero.create_tables
```

### Passo 4: Execute o servidor
```bash
python -m uvicorn fast_zero.app:app --reload --port 8000
```

✅ Pronto! A API está rodando em `http://localhost:8000`

---

## ▶️ Como Executar

### Iniciar o servidor (modo desenvolvimento com auto-reload)
```bash
python -m uvicorn fast_zero.app:app --reload --port 8000
```

### Iniciar o servidor (modo produção)
```bash
python -m uvicorn fast_zero.app:app --port 8000
```

### Acessar a API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🧪 Como Testar

### Forma 1: Pytest (Testes Automatizados)
Executa todos os 44 testes com cobertura completa:
```bash
python -m pytest tests/ -v
```

Testes de endpoints apenas:
```bash
python -m pytest tests/test_endpoints.py -v
```

Testes de queries apenas:
```bash
python -m pytest tests/test_queries.py -v
```

**Resultado**: 44 testes passando ✅

### Forma 2: Swagger UI (Interativo)
1. Acesse: http://localhost:8000/docs
2. Expanda um endpoint
3. Clique em "Try it out"
4. Preencha os dados
5. Clique em "Execute"

### Forma 3: cURL (Linha de Comando)

**Criar consumidor:**
```bash
curl -X POST "http://localhost:8000/consumidores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@example.com",
    "senha": "senha123",
    "contato": {
      "email": "joao@example.com",
      "telefone": "11999999999"
    }
  }'
```

**Listar consumidores:**
```bash
curl -X GET "http://localhost:8000/consumidores/"
```

**Atualizar consumidor:**
```bash
curl -X PUT "http://localhost:8000/consumidores/1" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva Atualizado",
    "email": "joao_novo@example.com",
    "senha": "novaSenha",
    "contato": {
      "email": "joao_novo@example.com",
      "telefone": "11988888888"
    }
  }'
```

**Deletar consumidor:**
```bash
curl -X DELETE "http://localhost:8000/consumidores/1"
```

---

## 🛣️ Endpoints Disponíveis

### Consumidores
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| POST | `/consumidores/` | Criar novo consumidor | ✅ |
| GET | `/consumidores/` | Listar todos consumidores | ✅ |
| PUT | `/consumidores/{id}` | Atualizar consumidor | ✅ |
| PATCH | `/consumidores/{id}` | Editar parcialmente | ✅ |
| DELETE | `/consumidores/{id}` | Deletar consumidor | ✅ |

### Empresas
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| POST | `/empresas/` | Criar nova empresa | ✅ |
| GET | `/empresas/` | Listar todas empresas | ✅ |
| PUT | `/empresas/{id}` | Atualizar empresa | ✅ |
| PATCH | `/empresas/{id}` | Editar parcialmente | ✅ |
| DELETE | `/empresas/{id}` | Deletar empresa | ✅ |

### Entregas
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| POST | `/entregas/` | Criar nova entrega | ✅ |
| GET | `/entregas/` | Listar todas entregas | ✅ |
| PATCH | `/entregas/{id}` | Atualizar status | ✅ |
| DELETE | `/entregas/{id}` | Deletar entrega | ✅ |

### Produtos
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| POST | `/produtos/` | Criar novo produto | ✅ |
| GET | `/produtos/` | Listar todos produtos | ✅ |
| PUT | `/produtos/{id}` | Atualizar produto | ✅ |
| PATCH | `/produtos/{id}` | Editar parcialmente | ✅ |
| DELETE | `/produtos/{id}` | Deletar produto | ✅ |

### Root
| Método | Endpoint | Descrição | Status |
|--------|----------|-----------|--------|
| GET | `/` | Health check | ✅ |

---

## 📁 Estrutura do Projeto

```
ap1-backend-fastapi-grupo-fgcmj/
├── fast_zero/
│   ├── __init__.py              # Inicialização do pacote
│   ├── app.py                   # Definição de endpoints (306 linhas)
│   ├── models.py                # Modelos ORM (65 linhas)
│   ├── schemas.py               # Schemas Pydantic (160+ linhas)
│   ├── database.py              # Configuração do banco
│   ├── create_tables.py          # Script de inicialização DB
│   └── __pycache__/
│
├── tests/
│   ├── conftest.py              # Configuração pytest (fixtures)
│   ├── test_endpoints.py        # 39 testes de endpoints
│   ├── test_queries.py          # 5 testes de queries
│   └── __pycache__/
│
├── requirements.txt             # Dependências do projeto
├── README.md                    # Documentação (este arquivo)
└── .gitignore                   # Arquivos ignorados git
```

---

## 🛠️ Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Propósito |
|------------|--------|----------|
| **Python** | 3.10+ | Linguagem principal |
| **FastAPI** | 0.128+ | Framework web assíncrono |
| **SQLAlchemy** | 2.0+ | ORM para banco dados |
| **Pydantic** | 2.0+ | Validação de dados |
| **Uvicorn** | 0.30+ | Servidor ASGI |
| **Pytest** | 9.0+ | Framework de testes |
| **Email-validator** | 2.1+ | Validação de emails |

### Banco de Dados
- **SQLite** (desenvolvimento)
- Compatível com PostgreSQL, MySQL (produção)

### Ferramentas
- **Git** - Controle de versão
- **Swagger UI** - Documentação interativa
- **cURL** - Testes CLI

---

## 📝 Exemplo Completo - Passo a Passo para Apresentação

### Cenário: Criar uma entrega de um laptop

**1️⃣ Criar um Consumidor:**
```bash
curl -X POST "http://localhost:8000/consumidores/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Santos",
    "email": "maria@example.com",
    "senha": "senha123",
    "contato": {
      "email": "maria@example.com",
      "telefone": "11987654321"
    }
  }'
```
Resposta: `{"id_consumidor": 1, ...}`

**2️⃣ Criar uma Empresa:**
```bash
curl -X POST "http://localhost:8000/empresas/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_empresa": "DroneLogistics",
    "email": "drone@example.com",
    "cnpj": "12.345.678/0001-90",
    "telefone": "1133333333",
    "senha": "empresapass123"
  }'
```
Resposta: `{"id_empresa": 1, ...}`

**3️⃣ Criar uma Entrega:**
```bash
curl -X POST "http://localhost:8000/entregas/" \
  -H "Content-Type: application/json" \
  -d '{
    "datahorainicio": "2026-02-25T10:00:00",
    "status": "em_transito",
    "id_empresa": 1
  }'
```
Resposta: `{"id_entrega": 1, ...}`

**4️⃣ Criar um Produto:**
```bash
curl -X POST "http://localhost:8000/produtos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome_produto": "Laptop Dell XPS",
    "peso": 2.5,
    "categoria": "eletrônicos",
    "id_consumidor": 1,
    "id_entrega": 1,
    "id_empresa": 1
  }'
```
Resposta: `{"id_produto": 1, ...}`

**5️⃣ Atualizar Status da Entrega:**
```bash
curl -X PATCH "http://localhost:8000/entregas/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "entregue",
    "datahoraconclusao": "2026-02-25T11:30:00"
  }'
```

### Gestão de Devoluções

Uma devolução pode ser solicitada quando a entrega estiver com status `Entregue` e tiver produtos associados ao consumidor informado.

**Solicitar devolução:**
```bash
curl -X POST "http://localhost:8000/consumidores/1/devolucoes/" \
  -H "Content-Type: application/json" \
  -d '{
    "id_entrega": 1,
    "produto_ids": [1],
    "motivo": "Produto com defeito"
  }'
```

A solicitação é registrada com data e status inicial `Solicitada`.
Os `produto_ids` devem identificar um ou mais produtos associados à entrega e ao consumidor. A resposta e a consulta da devolução incluem os produtos selecionados.

**Consultar devoluções do consumidor:**
```bash
curl -X GET "http://localhost:8000/consumidores/1/devolucoes/"
```

**Atualizar status da devolução:**
```bash
curl -X PATCH "http://localhost:8000/devolucoes/1" \
  -H "Content-Type: application/json" \
  -d '{"status": "Aprovada"}'
```

O status pode ser `Aprovada` ou `Recusada`. Como o projeto não possui autenticação, o `id_consumidor` na rota identifica o cliente, mas não comprova sua identidade; o endpoint de atualização também não restringe chamadas a administradores.

---

## ✅ Checklist de Verificação

- [ ] Python 3.10+ instalado
- [ ] Pip funcionando corretamente
- [ ] Repositório clonado localmente
- [ ] `pip install -r requirements.txt` executado com sucesso
- [ ] Banco de dados criado: `python -m fast_zero.create_tables`
- [ ] Servidor rodando: `python -m uvicorn fast_zero.app:app --reload --port 8000`
- [ ] Swagger acessível em: http://localhost:8000/docs
- [ ] Todos os testes passando: `python -m pytest tests/ -v` (44 passed)
- [ ] Endpoints testáveis via Swagger UI
- [ ] Endpoints testáveis via cURL
- [ ] Documentação atualizada

---

## 🐛 Troubleshooting - Soluções para Erros Comuns

### ❌ Erro: `ModuleNotFoundError: No module named 'fastapi'`
**Solução:** Instale as dependências
```bash
pip install -r requirements.txt
```

### ❌ Erro: `Port 8000 already in use`
**Solução:** Use uma porta diferente
```bash
python -m uvicorn fast_zero.app:app --reload --port 8001
```

### ❌ Erro: `sqlite3.OperationalError: no such table`
**Solução:** Crie o banco de dados
```bash
python -m fast_zero.create_tables
```

### ❌ Erro: `Email already registered` ao criar consumidor
**Solução:** Use um email único. Deletar registro anterior:
```bash
curl -X DELETE "http://localhost:8000/consumidores/1"
```

### ❌ Erro: `Foreign key constraint failed` ao criar produto
**Solução:** Verifique se consumidor, empresa e entrega existem:
```bash
# Listar recursos
curl -X GET "http://localhost:8000/consumidores/"
curl -X GET "http://localhost:8000/empresas/"
curl -X GET "http://localhost:8000/entregas/"
```

### ❌ Erro: `pytest: command not found`
**Solução:** Instale pytest ou use python -m
```bash
pip install pytest
# ou
python -m pytest tests/ -v
```

### ❌ Testes falhando com `AttributeError`
**Solução:** Verifique se o banco está limpo e rode novamente
```bash
python -m pytest tests/ -v --tb=short
```

---

## 📚 Documentação Adicional

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Pytest Docs](https://docs.pytest.org/)

---

## 👥 Equipe

- Desenvolvido pelo grupo FGCMJ
- Orientador: [Nome]
- Disciplina: Programação Web

---

## 📄 Licença

Este projeto é fornecido como está para fins educacionais.

---

**Última atualização**: 25 de Fevereiro de 2026


2.  Execute a aplicação:

```{=html}
<!-- uvicorn app:app --reload -->
```

3.  Acesse a documentação da API:

```{=html}
 http://localhost:8000
 http://localhost:8000/docs
```
