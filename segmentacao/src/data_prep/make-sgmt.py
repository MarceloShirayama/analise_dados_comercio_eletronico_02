import os
import sqlalchemy
import argparse
import pandas as pd
import sqlite3
import datetime
from dateutils import relativedelta
from olistlib.db.utils \
     import import_query, connect_db, execute_many_sql

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
date_init = datetime.datetime.strptime(args.date_end, '%Y-%m-%d') \
     - relativedelta(years=1)
date_init = date_init.strftime('%Y-%m-%d')

# date_end = args.date_end
# ano = int(date_end.split('-')[0]) - 1
# mes = int(date_end.split('-')[1])
# date_init = f'{ano}-{mes}-01'

# importa a query
query = import_query(os.path.join(DATA_PREP, 'segmentos.sql'))
query = query.format(date_init=date_init,
                    date_end=date_end)

print(query)

# # abrindo a conexão com o banco
# conn = connect_db('mariadb', os.path.join(BASE_DIR, '.env'))

# try:
#      create_query = f"""
#      CREATE TABLE olist.tb_seller_sgmt AS {query};"""
#      execute_many_sql(create_query, conn)
# except: 
#      insert_query = f"""
#      DELETE FROM olist.tb_seller_sgmt WHERE dt_sgmt = '{date_end}';
#      INSERT INTO olist.tb_seller_sgmt {query};"""
#      execute_many_sql(insert_query, conn, verbose=True)
