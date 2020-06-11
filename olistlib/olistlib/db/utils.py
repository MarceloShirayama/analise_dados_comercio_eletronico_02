import pandas as pd
import os
import sqlalchemy
from tqdm import tqdm


BASE_DIR = os.path.dirname(os.path.dirname(
     os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH = os.path.join(DATA_DIR, 'olist.db')

def import_query(path, **kwargs):
    """
    Função que realiza o import de uma query onde
    podem ser passados vários argumentos de import read()
    """
    with open(path, 'r', **kwargs) as file_query:
        query = file_query.read()
    return query

def connect_db():
    """Função para conexão com o banco de dados sqlite"""
    str_conn = 'sqlite:///{path}'.format(path=DB_PATH)
    connection = sqlalchemy.create_engine(str_conn)
    return connection

def execute_many_sql(sql, conn, verbose=False):
    """Função que executa a query"""
    if verbose:
        for i in tqdm(sql.split(';')[:-1]):
            conn.execute(i)
    else:
        for i in sql.split(';')[:-1]:
            conn.execute(i)
