from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_zero import models
from fast_zero.app import app
from fast_zero.database import Base, get_db


@pytest.fixture
def test_db(tmp_path):
    test_engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    session_factory = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield session_factory
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def client(test_db):
    def override_get_db():
        with test_db() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()


@pytest.fixture
def entrega_entregue(test_db):
    with test_db() as db:
        empresa = models.Empresa(
            nome_empresa="Drone Express",
            email="empresa@example.com",
            cnpj="12345678000199",
            telefone="11999999999",
            senha="senha",
        )
        consumidor = models.Consumidor(
            nome="Cliente",
            telefone="11988888888",
            email="cliente@example.com",
        )
        db.add_all([empresa, consumidor])
        db.flush()
        entrega = models.Entrega(
            codigo_rastreio="DX123456789BR",
            datahorainicio=datetime.now(),
            status="Entregue",
            id_empresa=empresa.id_empresa,
        )
        db.add(entrega)
        db.flush()
        produtos = [
            models.Produto(
                nome_produto=f"Produto {index}",
                peso=index,
                categoria="Geral",
                id_consumidor=consumidor.id_consumidor,
                id_entrega=entrega.id_entrega,
                id_empresa=empresa.id_empresa,
            )
            for index in (1, 2)
        ]
        db.add_all(produtos)
        db.commit()
        produto_ids = [produto.id_produto for produto in produtos]
        return consumidor.id_consumidor, entrega.id_entrega, produto_ids


def test_create_and_list_devolucao(client, entrega_entregue):
    consumidor_id, entrega_id, produto_ids = entrega_entregue
    produto_selecionado = produto_ids[0]
    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={
            "id_entrega": entrega_id,
            "produto_ids": [produto_selecionado],
            "motivo": "Produto com defeito",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["id_entrega"] == entrega_id
    assert payload["id_consumidor"] == consumidor_id
    assert payload["motivo"] == "Produto com defeito"
    assert payload["status"] == "Solicitada"
    assert payload["data_solicitacao"]
    assert [produto["id_produto"] for produto in payload["produtos"]] == [
        produto_selecionado
    ]

    response = client.get(f"/consumidores/{consumidor_id}/devolucoes/")
    assert response.status_code == 200
    assert [item["id_devolucao"] for item in response.json()["devolucoes"]] == [
        payload["id_devolucao"]
    ]
    assert [
        produto["id_produto"]
        for produto in response.json()["devolucoes"][0]["produtos"]
    ] == [produto_selecionado]


def test_return_rejects_product_not_associated_with_consumer(client, entrega_entregue):
    consumidor_id, entrega_id, produto_ids = entrega_entregue
    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={
            "id_entrega": entrega_id,
            "produto_ids": [produto_ids[0], 999999],
            "motivo": "Produto com defeito",
        },
    )

    assert response.status_code == 400


def test_return_requires_at_least_one_product(client, entrega_entregue):
    consumidor_id, entrega_id, _ = entrega_entregue
    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={"id_entrega": entrega_id, "produto_ids": [], "motivo": "Não gostei"},
    )

    assert response.status_code == 422


def test_cannot_request_return_before_delivery_is_received(client, test_db, entrega_entregue):
    consumidor_id, entrega_id, produto_ids = entrega_entregue
    with test_db() as db:
        entrega = db.query(models.Entrega).filter_by(id_entrega=entrega_id).first()
        entrega.status = "Em trânsito"
        db.commit()

    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={"id_entrega": entrega_id, "produto_ids": produto_ids, "motivo": "Não gostei"},
    )

    assert response.status_code == 400


def test_cannot_request_return_for_another_consumers_delivery(
    client, test_db, entrega_entregue
):
    _, entrega_id, produto_ids = entrega_entregue
    with test_db() as db:
        consumidor = models.Consumidor(nome="Outro cliente", telefone="11977777777")
        db.add(consumidor)
        db.commit()
        consumidor_id = consumidor.id_consumidor

    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={"id_entrega": entrega_id, "produto_ids": produto_ids, "motivo": "Não gostei"},
    )

    assert response.status_code == 400


@pytest.mark.parametrize("status", ["Aprovada", "Recusada"])
def test_admin_can_update_status_only_once(client, entrega_entregue, status):
    consumidor_id, entrega_id, produto_ids = entrega_entregue
    created = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={
            "id_entrega": entrega_id,
            "produto_ids": produto_ids,
            "motivo": "Produto com defeito",
        },
    )
    devolucao_id = created.json()["id_devolucao"]

    response = client.patch(
        f"/devolucoes/{devolucao_id}",
        json={"status": status},
    )
    assert response.status_code == 200
    assert response.json()["status"] == status

    repeated = client.patch(
        f"/devolucoes/{devolucao_id}",
        json={"status": "Recusada" if status == "Aprovada" else "Aprovada"},
    )
    assert repeated.status_code == 400


def test_status_update_rejects_other_values(client, entrega_entregue):
    consumidor_id, entrega_id, produto_ids = entrega_entregue
    created = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={
            "id_entrega": entrega_id,
            "produto_ids": produto_ids,
            "motivo": "Produto com defeito",
        },
    )

    response = client.patch(
        f"/devolucoes/{created.json()['id_devolucao']}",
        json={"status": "Solicitada"},
    )
    assert response.status_code == 422


def test_return_reason_cannot_be_blank(client, entrega_entregue):
    consumidor_id, entrega_id, produto_ids = entrega_entregue

    response = client.post(
        f"/consumidores/{consumidor_id}/devolucoes/",
        json={"id_entrega": entrega_id, "produto_ids": produto_ids, "motivo": "  "},
    )

    assert response.status_code == 422
