from airflow.models import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split as sk_train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, log_loss, classification_report
import pickle


def prepare_data():
    print("-----Inside prepare_data component----")
    df = pd.read_csv("https://raw.githubusercontent.com/TripathiAshutosh/dataset/main/iris.csv")
    df = df.dropna()
    df.to_csv('final_df.csv', index=False)


def split_train_test():
    print("---Inside split_train_test----")
    final_data = pd.read_csv('final_df.csv')
    target_class = "class"
    x = final_data.loc[:, final_data.columns != target_class]
    y = final_data.loc[:, target_class].values.ravel()
    x_train, x_test, y_train, y_test = sk_train_test_split(x, y, test_size=0.3, stratify=y, random_state=42)

    np.save('x_train.npy', x_train)
    np.save('x_test.npy', x_test)
    np.save('y_train.npy', y_train)
    np.save('y_test.npy', y_test)

    print("\n--- x_train ---\n", x_train)
    print("\n--- x_test ---\n", x_test)
    print("\n--- y_train ---\n", y_train)
    print("\n--- y_test ---\n", y_test)


def training_basic_classifier():
    from sklearn.linear_model import LogisticRegression
    x_train = np.load('x_train.npy', allow_pickle=True)
    y_train = np.load('y_train.npy', allow_pickle=True)

    classifier = LogisticRegression(max_iter=500, multi_class='multinomial')
    classifier.fit(x_train, y_train)

    with open("model.pkl", 'wb') as f:
        pickle.dump(classifier, f)

    print("\nLogistic Regression has been trained")


def predict_on_test_data():
    print("----Inside predict_on_test_data----")
    with open("model.pkl", 'rb') as f:
        logistic_reg_model = pickle.load(f)

    x_test = np.load("x_test.npy", allow_pickle=True)
    y_pred = logistic_reg_model.predict(x_test)
    np.save("y_pred.npy", y_pred)

    print("\n---- Predicted Classes ----\n", y_pred)


def predict_prob_on_test_data():
    print("----Inside predict_prob_on_test_data----")
    with open('model.pkl', 'rb') as f:
        logistic_reg_model = pickle.load(f)

    x_test = np.load("x_test.npy", allow_pickle=True)
    y_pred_prob = logistic_reg_model.predict_proba(x_test)
    np.save("y_pred_prob.npy", y_pred_prob)

    print("\n--- Predicted Probabilities ---\n", y_pred_prob)


def get_matrices():
    print("---Inside get_matrices----")
    y_test = np.load("y_test.npy", allow_pickle=True)
    y_pred = np.load("y_pred.npy", allow_pickle=True)
    y_pred_prob = np.load("y_pred_prob.npy", allow_pickle=True)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='micro')
    recall = recall_score(y_test, y_pred, average="micro")
    entropy = log_loss(y_test, y_pred_prob)

    print("\nModel Metrics:\n", {"accuracy": acc, "precision": prec, "recall": recall, "entropy": entropy})
    print("\nClassification Report:\n", classification_report(y_test, y_pred))



dag1 = DAG(
    dag_id="ml_pipeline",
    start_date=datetime(2023, 12, 1),  # Replace with your desired start date
    schedule_interval="@daily",
    catchup=False,
)

# Define the tasks
task_prepare_data = PythonOperator(
    task_id="prepare_data",
    python_callable=prepare_data,
    dag=dag1
)

task_train_test_split = PythonOperator(
    task_id="train_test_split",
    python_callable=split_train_test,
    dag=dag1
)

task_training_basic_classifier = PythonOperator(
    task_id="training_basic_classifier",
    python_callable=training_basic_classifier,
    dag=dag1
)

task_predict_on_test_data = PythonOperator(
    task_id="predict_on_test_data",
    python_callable=predict_on_test_data,
    dag=dag1
)

task_predict_prob_on_test_data = PythonOperator(
    task_id="predict_prob_on_test_data",
    python_callable=predict_prob_on_test_data,
    dag=dag1
)

task_get_matrices = PythonOperator(
    task_id="get_matrices",
    python_callable=get_matrices,
    dag=dag1
)

# Set task dependencies
task_prepare_data >> task_train_test_split >> \
task_training_basic_classifier >> task_predict_on_test_data >> \
task_predict_prob_on_test_data >> task_get_matrices