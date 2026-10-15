import random
import string
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table, event
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base


devolucao_produtos = Table(
    "devolucao_produtos",
    Base.metadata,
    Column(
        "id_devolucao",
        Integer,
        ForeignKey("devolucoes.id_devolucao", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "id_produto",
        Integer,
        ForeignKey("produtos.id_produto", ondelete="CASCADE"),
        primary_key=True,
    ),
)


def _gerar_codigo_rastreio() -> str:
    """Gera código no formato AA999999999BR — ex: DX748291035BR"""
    prefixo = "".join(random.choices(string.ascii_uppercase, k=2))
    numero  = "".join(random.choices(string.digits, k=9))
    return f"{prefixo}{numero}BR"


class Consumidor(Base):
    __tablename__ = "consumidores"

    id_consumidor = Column(Integer, primary_key=True, index=True)
    nome          = Column(String, nullable=False)
    telefone      = Column(String, nullable=False)
    email         = Column(String, nullable=True)   # apenas contato, não é login

    produtos = relationship("Produto", back_populates="consumidor", cascade="all, delete-orphan")
    devolucoes = relationship(
        "Devolucao", back_populates="consumidor", cascade="all, delete-orphan"
    )


class Empresa(Base):
    __tablename__ = "empresa"

    id_empresa   = Column(Integer, primary_key=True, index=True)
    nome_empresa = Column(String, nullable=False)
    email        = Column(String, unique=True, nullable=False, index=True)
    cnpj         = Column(String, unique=True, nullable=False)
    telefone     = Column(String, nullable=False)
    senha        = Column(String, nullable=False)

    produtos = relationship("Produto", back_populates="empresa", cascade="all, delete-orphan")
    entregas = relationship("Entrega", back_populates="empresa", cascade="all, delete-orphan")


class Entrega(Base):
    __tablename__ = "entregas"

    id_entrega        = Column(Integer, primary_key=True, index=True)
    codigo_rastreio   = Column(String, unique=True, nullable=False, index=True)
    datahorainicio    = Column(DateTime, default=datetime.utcnow, nullable=False)
    datahoraconclusao = Column(DateTime, nullable=True)
    status            = Column(String, nullable=False)

    id_empresa = Column(Integer, ForeignKey("empresa.id_empresa"), nullable=False)
    empresa    = relationship("Empresa", back_populates="entregas")

    produtos = relationship("Produto", back_populates="entrega")  # sem cascade: produto existe antes da entrega
    devolucoes = relationship(
        "Devolucao", back_populates="entrega", cascade="all, delete-orphan"
    )


@event.listens_for(Entrega, "before_insert")
def _set_codigo(mapper, connection, target):
    if not target.codigo_rastreio:
        target.codigo_rastreio = _gerar_codigo_rastreio()


class Produto(Base):
    __tablename__ = "produtos"

    id_produto   = Column(Integer, primary_key=True, index=True)
    nome_produto = Column(String, nullable=False)
    peso         = Column(Float, nullable=False)
    categoria    = Column(String, nullable=False)

    id_consumidor = Column(Integer, ForeignKey("consumidores.id_consumidor"), nullable=False)
    consumidor    = relationship("Consumidor", back_populates="produtos")

    # Nullable: produto existe antes de ter uma entrega
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"), nullable=True)
    entrega    = relationship("Entrega", back_populates="produtos")

    id_empresa = Column(Integer, ForeignKey("empresa.id_empresa"), nullable=False)
    empresa    = relationship("Empresa", back_populates="produtos")
    devolucoes = relationship(
        "Devolucao", secondary=devolucao_produtos, back_populates="produtos"
    )


class Devolucao(Base):
    __tablename__ = "devolucoes"

    id_devolucao = Column(Integer, primary_key=True, index=True)
    id_entrega = Column(Integer, ForeignKey("entregas.id_entrega"), nullable=False)
    id_consumidor = Column(Integer, ForeignKey("consumidores.id_consumidor"), nullable=False)
    motivo = Column(String, nullable=False)
    data_solicitacao = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    status = Column(String, default="Solicitada", nullable=False)

    entrega = relationship("Entrega", back_populates="devolucoes")
    consumidor = relationship("Consumidor", back_populates="devolucoes")
    produtos = relationship(
        "Produto", secondary=devolucao_produtos, back_populates="devolucoes"
    )