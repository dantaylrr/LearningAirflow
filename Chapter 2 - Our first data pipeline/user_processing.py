# recall, all of this is done inside a vm - so is for my own reference

from airflow.models import DAG # always done
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}
# we can set default_args if we want

# define our DAG
with DAG('user_processing', schedule_interval='@daily',
        default_args=default_args,
        catchup=False) as dag: # set dag parameters

# define tasks/operators

# create a table in the sqlite database - we can use the sqlite operator to do this & standard SQL code

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE users (
                firstname TEXT NOT NULL,
                last   name TEXT NOT NULL,
                country TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
            '''
    )