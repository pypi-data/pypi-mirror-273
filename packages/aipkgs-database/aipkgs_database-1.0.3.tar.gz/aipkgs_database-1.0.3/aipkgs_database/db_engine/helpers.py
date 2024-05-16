# https://docs.sqlalchemy.org/en/14/core/connections.html
# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
# https://chartio.com/resources/tutorials/how-to-execute-raw-sql-in-sqlalchemy/
import os

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy import inspect
from sqlalchemy.engine import Engine, Inspector
from sqlalchemy.orm import sessionmaker, Session


class DBEngine:
    def __init__(self, db_path: str):
        self.engine: Engine = DBEngine.fire_engine(db_path=db_path, echo=True)
        self.inspector: Inspector = DBEngine.fire_inspector(self.engine)
        self.session: Session = DBEngine.fire_session(engine=self.engine)

    def exec(self, query_str: str):
        with self.engine.connect() as connection:
            result = connection.execute(text(query_str))
            return result

    def query_table(self, name: str):
        with self.inspector as inspector:
            results = inspector.get_columns(name)
            return results

    def run_transaction(self, table: Table, columns: dict):
        with self.engine.begin() as connection:
            r1 = connection.execute(table.select())
            connection.execute(table.insert(), columns)

    @staticmethod
    def fire_engine(db_path: str, echo: bool = None) -> Engine:
        _engine = create_engine(db_path, echo=echo or False)
        return _engine

    @staticmethod
    def fire_inspector(engine) -> Inspector:
        _inspector = inspect(engine)
        return _inspector

    @staticmethod
    def fire_session(engine) -> Session:
        _session_class = sessionmaker(bind=engine)
        # _session.configure(bind=engine)
        return _session_class()
