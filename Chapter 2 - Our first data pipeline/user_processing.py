# recall, all of this is done inside a vm - so is for my own reference

from airflow.models import DAG # always done
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime
from pandas import json_normalize
import json

# we can set default_args if we want

default_args = {
    'start_date': datetime(2020, 1, 1)
}

# define any python functions we want to call using our PythonOperator

def _processing_user(ti):
    users = ti.xcom_pull(task_ids=['extracting_user']) # task_id of the previous task, getting our data to use
    # we will learn more about ti (task instances) & xcom's later
    if not len(users) or 'results' not in users[0]:
        raise ValueError('User is empty')
    user = users[0]['results'][0]
    # json_normalize converts our json response to a pandas dataframe
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'password': user['login']['password'],
        'email': user['email']
    })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

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
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                last   name TEXT NOT NULL,
                country TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
            '''
    )

# next task, let's check whether the api is available

    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/' # the page that is going to be checked
    )

# next task, let's do an api GET call to get our data

    extracting_user = SimpleHttpOperator(
        task_id='extracting_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

# next task, let's process the data from our GET request to only
# get the fields we made in our table 'users'

    processing_user = PythonOperator(
        task_id='processing_user',
        python_callable=_processing_user # specify the function that we want to call - defined at the start of the script
    )

# our final task, let's populate the sqlite table with the .csv we created

    storing_user = BashOperator(
        task_id='storing_user',
        bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /home/airflow/airflow/airflow.db'
    )

# bash command... specify comma(,) separator (it's a .csv file), then import the .csv into table 'users'
# then specify the airflow db

# define our dependencies, or the order in which to execute the tasks

    creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user