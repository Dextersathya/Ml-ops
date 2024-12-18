from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
import requests


# Function to print a welcome message
def print_welcome():
    print("Welcome to Airflow!")


# Function to print the current date
def print_date():
    print("Today is {}".format(datetime.today().date()))


# Function to fetch and print a random quote
def fetch_random_quote():
    response = requests.get("https://zenquotes.io/api/random")
    if response.status_code == 200:
        data = response.json()  # The response is a list
        if data and isinstance(data, list):  # Ensure it's a non-empty list
            quote = data[0]["q"]  # Get the quote text
            author = data[0]["a"]  # Get the author
            print(f'Quote of the day: "{quote}" - {author}')
        else:
            print("Unexpected response format.")
    else:
        print("Failed to fetch the quote. Status code:", response.status_code)


# Define the DAG
dag = DAG(
    "welcome_dag",
    default_args={"start_date": days_ago(1)},
    schedule_interval="0 23 * * *",  # Daily at 11 PM
    catchup=False,
)

# Define tasks
print_welcome_task = PythonOperator(
    task_id="print_welcome",
    python_callable=print_welcome,
    dag=dag,
)

print_date_task = PythonOperator(
    task_id="print_date",
    python_callable=print_date,
    dag=dag,
)

print_random_quote_task = PythonOperator(
    task_id="print_random_quote",
    python_callable=fetch_random_quote,
    dag=dag,
)

# Set task dependencies
print_welcome_task >> print_date_task >> print_random_quote_task
