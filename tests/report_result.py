import os
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import BigInteger
from sqlalchemy.orm import Session
from sqlalchemy import insert, select
import pandas as pd
from logger_tests import logger

PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_HOST = os.getenv("PG_HOST")
PG_DB = os.getenv("PG_DB")
PG_PORT = int(os.getenv("PG_PORT", 5432))
P2F_CLIENT_TEST_RUN_ID = os.getenv("P2F_CLIENT_TEST_RUN_ID")
P2F_TEST_EMAIL = os.getenv("P2F_TEST_EMAIL")

connection_str = f"postgresql+psycopg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
engine = create_engine(connection_str)
baseSQL = declarative_base()

class report_results(baseSQL):
    __tablename__ = f"p2f_client_test_{P2F_CLIENT_TEST_RUN_ID}"
    pk: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    status_code: Mapped[int] = mapped_column(Integer, nullable=True)
    test_name: Mapped[str] = mapped_column(Text, nullable=False)
    output_text: Mapped[str] = mapped_column(Text, nullable=True)
    email: Mapped[str] = mapped_column(Text, nullable=False)

baseSQL.metadata.create_all(engine)

def add_report(test_name:str, output_text:str, status_code: int=0):
    output_text = str(output_text)
    with Session(engine) as session:
        stmt = insert(report_results)
        stmt = stmt.values(
            status_code=status_code,
            test_name=test_name,
            output_text=output_text,
            email=P2F_TEST_EMAIL
        )
        session.execute(stmt)
        session.commit()

def dump_reports():
    with Session(engine) as session:
        stmt = select(report_results)
        df = pd.read_sql(stmt, engine)
    output = StringIO()
    df.to_csv(output)
    logger.debug(output.getvalue())
