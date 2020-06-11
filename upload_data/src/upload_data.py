import os
from pprint import pprint
import pandas as pd
import sqlalchemy



# diretórios e sub-diretórios do projeto
BASE_DIR = os.path.dirname(
     os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data')

print(f"base_dir: {BASE_DIR}")
print(f"data_dir: {DATA_DIR}")

files_names = [i for i in os.listdir(DATA_DIR) if i.endswith('.csv')]

# abrindo a conexão com o banco
str_conn = 'sqlite:///{path}'
str_conn = str_conn.format(path=os.path.join(DATA_DIR, 'olist.db'))
conn = sqlalchemy.create_engine(str_conn)

for i in files_names:
    df_tmp = pd.read_csv(os.path.join(DATA_DIR, i))
    table_name = "tb_" + i.strip(".csv").replace("olist_", "").\
         replace("_dataset", "")
    df_tmp.to_sql(table_name, conn)
