from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    run_pipeline = BashOperator(
        task_id="run_weather_pipeline",
        bash_command="python3 /opt/airflow/src/main.py"
    )



