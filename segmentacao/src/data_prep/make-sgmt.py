import os
import sqlalchemy
import argparse
import pandas as pd
import sqlite3
from utils.utils import import_query, connect_db, execute_many_sql


# diretórios e sub-diretórios do projeto
DATA_PREP = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(
     os.path.dirname(os.path.dirname(DATA_PREP)))

parser = argparse.ArgumentParser()
parser.add_argument(
     '--date_end',
     '-e', help='Data fim da extração',
     default='2018-06-01')
args = parser.parse_args()

date_end = args.date_end
ano = int(date_end.split('-')[0]) - 1
mes = int(date_end.split('-')[1])
date_init = f'{ano}-{mes}-01'

# importa a query
query = import_query(os.path.join(DATA_PREP, 'segmentos.sql'))
query = query.format(date_init = date_init,
                    date_end = date_end)

# abrindo a conexão com o banco
conn = connect_db()

create_query = f"""
CREATE TABLE tb_seller_sgmt AS 
{query}
;"""

insert_query = f"""
DELETE FROM tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
INSERT INTO tb_seller_sgmt 
{query}
;"""

try:
    execute_many_sql(create_query, conn)
except: 
    execute_many_sql(insert_query, conn, verbose=True)
