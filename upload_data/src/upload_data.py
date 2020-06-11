import os
from pprint import pprint
import pandas as pd
import sqlalchemy
import argparse
from olistlib.db.utils import import_query, \
     connect_db, execute_many_sql


# diretórios e sub-diretórios do projeto
UP_DIR = os.path.dirname(
     os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(
     os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(UP_DIR, 'data')

print(f"up_dir: {UP_DIR}")
print(f"base_dir: {BASE_DIR}")
print(f"data_dir: {DATA_DIR}")

# encontrando os arquivos de dados
files_names = [i for i in os.listdir(DATA_DIR) \
     if i.endswith('.csv')]

# abrindo a conexão com o banco
conn = connect_db('mariadb', os.path.join(BASE_DIR, '.env'))

for i in files_names:
     print(i)
     df_tmp = pd.read_csv(os.path.join(DATA_DIR, i))
     table_name = "tb_" + i.strip(".csv").\
          replace("olist_", "").replace("_dataset", "")
     df_tmp.to_sql(
          table_name, 
          conn,
          schema='olist',
          if_exists='replace',
          index=False
     )
