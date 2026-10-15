from .database import engine, Base
from . import models


def create_all():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_all()
    print("Tabelas criadas com sucesso em fast_zero.db")
