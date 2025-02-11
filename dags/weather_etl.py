import requests
import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.providers.postgres.hooks.postgres import PostgresHook


API_KEY = " YOUR API KEY"
CITY = "Caratinga,BR"
ENDPOINT = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def extract_data(**kwargs):
    response = requests.get(ENDPOINT)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
        kwargs["ti"].xcom_push(key="weather_data", value=data)
    else:
        raise Exception(f"Error accessing the API: {response.status_code}")
        
def transform_data(**kwargs):
    data = kwargs["ti"].xcom_pull(key="weather_data", task_ids="extract_data")
    if data:
        transformed_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
        }
        print("Transformed data:", transformed_data)
        kwargs['ti'].xcom_push(key='transformed_data', value=transformed_data)
    else:
        raise Exception("No data found to transform.")
    
def load_data(**kwargs):
    transformed_data = kwargs["ti"].xcom_pull(key="transformed_data", task_ids="transform_data")
    if transformed_data:
        
        pg_hook = PostgresHook(postgres_conn_id="postgres_default")
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            city VARCHAR(50),
            temperature REAL,
            humidity INTEGER,
            weather VARCHAR(100),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        
        insert_query = """
        INSERT INTO weather_data (city, temperature, humidity, weather)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (
            transformed_data['city'],
            transformed_data['temperature'],
            transformed_data['humidity'],
            transformed_data['weather']
        ))
        
        conn.commit()
        cursor.close()
        conn.close()
        print("Data successfully loaded into PostgreSQL!")
        
        
    else:
        raise Exception("No data found to load.")
    
with DAG(
    "weather_data_pipeline",
    start_date=datetime(2025, 2, 10),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
        provide_context=True
    )
    
    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        provide_context=True
    )
    
    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
        provide_context=True
    )
    
    extract_task >> transform_task >> load_task
