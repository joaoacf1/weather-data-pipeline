from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_hello():
    print("Hello from Airflow!")
    
default_args = {
    'start_date': datetime(2025, 2, 10),
    'catchup': False
}

with DAG(
    'test_dag',
    default_args=default_args,
    schedule_interval='@daily',
    tags=['test']
) as dag:
    
    task_hello = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello
    )
    
    
    # ENDPOINT: https://api.openweathermap.org/data/2.5/weather?q=London&appid=6f62b378b4e81a475fb67c24e5e2367c