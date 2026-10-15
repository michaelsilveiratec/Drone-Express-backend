from typing import Annotated, Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints, field_validator
from datetime import datetime


# ─── Consumidor ───────────────────────────────────────────────────────────────
# Consumidor não tem login — apenas dados de contato

class ConsumidorSchema(BaseModel):
    nome:     str
    telefone: str
    email:    Optional[str] = None   # e-mail de contato, não obrigatório

class ConsumidorPublic(BaseModel):
    id_consumidor: int
    nome:          str
    telefone:      str
    email:         Optional[str]
    class Config:
        orm_mode = True

class ConsumidorList(BaseModel):
    consumidores: list[ConsumidorPublic]

class ConsumidorUpdate(BaseModel):
    nome:     Optional[str] = None
    telefone: Optional[str] = None
    email:    Optional[str] = None


# ─── Empresa ──────────────────────────────────────────────────────────────────

class EmpresaSchema(BaseModel):
    nome_empresa: str
    email:        EmailStr
    cnpj:         str
    telefone:     str
    senha:        str

class EmpresaPublic(BaseModel):
    id_empresa:   int
    nome_empresa: str
    email:        EmailStr
    cnpj:         str
    telefone:     str
    class Config:
        orm_mode = True

class EmpresaList(BaseModel):
    empresas: list[EmpresaPublic]

class EmpresaUpdate(BaseModel):
    nome_empresa: Optional[str]      = None
    email:        Optional[EmailStr] = None
    cnpj:         Optional[str]      = None
    telefone:     Optional[str]      = None
    senha:        Optional[str]      = None


# ─── Produto ──────────────────────────────────────────────────────────────────
# Produto é criado SEM entrega. id_entrega é preenchido depois.

class ProdutoSchema(BaseModel):
    nome_produto:  str
    peso:          float
    categoria:     str
    id_consumidor: int
    id_empresa:    int
    # id_entrega não vai no schema de criação — produto nasce "livre"

class ProdutoPublic(BaseModel):
    id_produto:    int
    nome_produto:  str
    peso:          float
    categoria:     str
    id_consumidor: int
    id_entrega:    Optional[int]   # None = produto ainda não despachado
    id_empresa:    int
    class Config:
        orm_mode = True

class ProdutoList(BaseModel):
    Produtos: list[ProdutoPublic]

class ProdutoUpdate(BaseModel):
    nome_produto:  Optional[str]   = None
    peso:          Optional[float] = None
    categoria:     Optional[str]   = None
    id_consumidor: Optional[int]   = None
    id_empresa:    Optional[int]   = None
    # id_entrega NÃO é editável por aqui — use POST /entregas/{id}/produtos


# ─── Entrega ──────────────────────────────────────────────────────────────────

class EntregaSchema(BaseModel):
    datahorainicio:    datetime
    datahoraconclusao: Optional[datetime] = None   # previsão já na criação
    status:            str
    id_empresa:        int
    produto_ids:       list[int] = []   # produtos livres a associar na criação

class EntregaPublic(BaseModel):
    id_entrega:        int
    codigo_rastreio:   str
    datahorainicio:    datetime
    datahoraconclusao: Optional[datetime]
    status:            str
    id_empresa:        int
    nome_empresa:      str             # retorna o nome, não só o id
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        data = {
            "id_entrega":        obj.id_entrega,
            "codigo_rastreio":   obj.codigo_rastreio,
            "datahorainicio":    obj.datahorainicio,
            "datahoraconclusao": obj.datahoraconclusao,
            "status":            obj.status,
            "id_empresa":        obj.id_empresa,
            "nome_empresa":      obj.empresa.nome_empresa if obj.empresa else "",
        }
        return cls(**data)

class EntregaList(BaseModel):
    entregas: list[EntregaPublic]

class EntregaUpdate(BaseModel):
    datahorainicio:    Optional[datetime] = None
    datahoraconclusao: Optional[datetime] = None
    status:            Optional[str]      = None

class AssociarProdutosSchema(BaseModel):
    produto_ids: list[int]


# ─── Devoluções ───────────────────────────────────────────────────────────────

class DevolucaoCreate(BaseModel):
    id_entrega: int
    produto_ids: list[int] = Field(min_length=1)
    motivo: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]

    @field_validator("produto_ids")
    @classmethod
    def validar_produtos_unicos(cls, produto_ids: list[int]) -> list[int]:
        if len(produto_ids) != len(set(produto_ids)):
            raise ValueError("A lista de produtos não pode conter itens duplicados")
        return produto_ids

class ProdutoDevolucaoPublic(BaseModel):
    id_produto: int
    nome_produto: str
    peso: float
    categoria: str

    model_config = ConfigDict(from_attributes=True)

class DevolucaoPublic(BaseModel):
    id_devolucao: int
    id_entrega: int
    id_consumidor: int
    motivo: str
    data_solicitacao: datetime
    status: str
    produtos: list[ProdutoDevolucaoPublic]

    model_config = ConfigDict(from_attributes=True)

class DevolucaoList(BaseModel):
    devolucoes: list[DevolucaoPublic]

class DevolucaoStatusUpdate(BaseModel):
    status: Literal["Aprovada", "Recusada"]


# ─── Rastreio público (endpoint /rastrear) ────────────────────────────────────

class ProdutoRastreioPublic(BaseModel):
    nome_produto: str
    peso:         float
    categoria:    str
    class Config:
        orm_mode = True

class RastreioPublic(BaseModel):
    codigo_rastreio:   str
    status:            str
    nome_empresa:      str
    datahorainicio:    datetime
    datahoraconclusao: Optional[datetime]
    produtos:          list[ProdutoRastreioPublic]


# ─── Utilitários ──────────────────────────────────────────────────────────────

class Message(BaseModel):
    message: str