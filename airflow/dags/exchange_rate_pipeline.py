from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from clean_data import clean_data

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'exchange_rate_etl',
    default_args=default_args,
    start_date=datetime(2024, 12, 7),
    schedule_interval='@daily',
    catchup=False
)

# Task 1: Download exchange rate data
download_task = BashOperator(
    task_id='download_file',
    bash_command='curl -o /tmp/xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata',
    dag=dag,
)

# Task 2: Clean the data
clean_data_task = PythonOperator(
    task_id='clean_data',
    python_callable=clean_data,
    dag=dag,
)

# Task 3: Send an email notification
send_email_task = EmailOperator(
    task_id='send_email',
    to='usathya1510@gmail.com',
    subject='Exchange Rate Download - Successful',
    html_content='The Exchange Rate data has been successfully downloaded, cleaned, and saved.',
    dag=dag,
)

# Define task dependencies
download_task >> clean_data_task >> send_email_task
