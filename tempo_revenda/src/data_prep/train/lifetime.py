import os
import pandas as pd
from utils.utils import import_query, connect_db, execute_many_sql


# diretórios e sub-diretórios do projeto
BASE_DIR = os.path.dirname(
     os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SQL_DIR = os.path.join(BASE_DIR, 'src', 'sql')

# importa a query
query = import_query(os.path.join(SQL_DIR, 'lifetime.sql'))

# abrindo a conexão com o banco
conn = connect_db()

# execução da query no banco
df = pd.read_sql_query(query, conn)

# exporta o resultado da query em csv
df.to_csv(os.path.join(
    DATA_DIR, 'lifetime.csv'), sep=';', index=False)
