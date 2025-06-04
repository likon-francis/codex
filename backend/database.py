from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("sqlite:///codex.db", echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    return Session(engine)
