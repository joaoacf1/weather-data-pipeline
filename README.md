# 🌦️ Weather Data Pipeline with Airflow and PostgreSQL

This project is a data pipeline built with **Apache Airflow**, **Docker**, and **PostgreSQL**.  
It collects weather data daily from a public weather API and stores it in a PostgreSQL database for further analysis.  
This project showcases my skills in building **scalable ETL pipelines** using modern data engineering tools.

---

## 🚀 Tech Stack
- **Apache Airflow**: Task scheduling and pipeline orchestration.  
- **Docker**: Containerization for seamless development and deployment.  
- **PostgreSQL**: Database to store and query the collected weather data.  
- **Python**: For data extraction and transformation.  

---

## 📊 Features
- Automatically collects **weather data** every day.  
- Stores the data in a **PostgreSQL** database for analysis.  
- **Fully containerized** using Docker for easier setup and deployment.  
- Easily extendable for additional data sources or transformations.

## 🛠️ Setup and Installation
### Prerequisites
- **Docker** and **Docker Compose** installed on your machine.

### Steps to Run the Project:
1. Clone the repository:
   ```bash
   git clone https://github.com/joaoacf1/weather-data-pipeline.git
   cd weather-data-pipeline

2. Start the services with Docker Compose:
   ```bash
   docker-compose up -d

3. **Access the Airflow Web Interface:**  
   Open your browser and navigate to `http://localhost:8080`.  
   Use the default login credentials:  
   - **Username:** `airflow`  
   - **Password:** `airflow`

4. **Set up the PostgreSQL connection in Airflow:**  
   - Go to the Airflow **Admin > Connections** page.  
   - Click the **+ (Add Connection)** button.  
   - Configure the connection as follows:  
     - **Connection ID:** `postgres_default`  
     - **Connection Type:** `Postgres`  
     - **Host:** `postgres`  
     - **Schema:** `airflow`  
     - **Login:** `airflow`  
     - **Password:** `airflow`  
     - **Port:** `5432`  
   - Save the connection.

5. **Trigger the DAG:**  
   - In the Airflow UI, enable and trigger the DAG named `weather_data_etl` to start the pipeline manually.

---

### 🏃 Running the Pipeline:

The pipeline runs daily to fetch weather data and store it in the PostgreSQL database.
You can also trigger it manually from the Airflow web interface.

---

### 🔍 Querying the Data

You can explore the data stored in PostgreSQL by connecting to the database. Here are two ways to do that:

1. **Using the terminal:**

   ```bash
   docker exec -it weather-data-pipeline-postgres-1 psql -U airflow -d airflow
   ´´´
   Once connected, run the following SQL query:

   ```sql
   SELECT * FROM weather_data;
   ```

2. **Using a tool like DataGrip or DBeaver:**

Connect to the PostgreSQL instance with the following details:

- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `airflow`
- **Username:** `airflow`
- **Password:** `airflow`

---

### Example of the collected data:

| city      | temperature | humidity | Weather          | timestamp                  |
|-----------|-------------|----------|------------------|----------------------------|
| Caratinga | 26.82       | 60       | overcast clouds  | 2025-02-11 13:00:30.139280 |
| London    | 5.54        | 81       | overcast clouds  | 2025-02-12 14:59:41.921171 |



![airflow](https://github.com/user-attachments/assets/6b150eae-c961-47e5-a4b9-3d49988fe1b1)

