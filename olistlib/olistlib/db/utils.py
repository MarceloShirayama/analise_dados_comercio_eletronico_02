import pandas as pd
import os
import sqlalchemy
from tqdm import tqdm
import dotenv


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

def connect_db(db_name, dotenv_path=os.path.expanduser('~/.env')):
    """Função para conexão com o banco de dados sqlite"""

    dotenv.load_dotenv(dotenv_path)

    host = os.getenv("HOST_" + db_name.upper())
    port = os.getenv("PORT_" + db_name.upper())
    user = os.getenv("USER_" + db_name.upper())
    pswd = os.getenv("PSWD_" + db_name.upper())

    if db_name == 'mariadb':
        str_conn = f"mysql+pymysql://{user}:{pswd}@{host}:{port}"
        
    return sqlalchemy.create_engine(str_conn)
    
def execute_many_sql(sql, conn, verbose=False):
    """Função que executa a query"""
    if verbose:
        for i in tqdm(sql.split(';')[:-1]):
            conn.execute(i)
    else:
        for i in sql.split(';')[:-1]:
            conn.execute(i)
