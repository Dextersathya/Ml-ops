# ML Pipeline with Apache Airflow

This repository contains an end-to-end Machine Learning pipeline implemented using Apache Airflow. The pipeline performs the following tasks:

1. **Data Preparation**
2. **Train-Test Split**
3. **Model Training**
4. **Prediction on Test Data**
5. **Prediction Probabilities**
6. **Evaluation Metrics**

## Prerequisites

- Python 3.7 or higher
- Apache Airflow
- Required Python libraries (see [Requirements](#requirements))

## Pipeline Overview

The pipeline is defined in the `ml_pipeline` DAG and includes the following tasks:

1. **`prepare_data`**: Downloads and preprocesses the dataset.
2. **`train_test_split`**: Splits the dataset into training and testing sets.
3. **`training_basic_classifier`**: Trains a Logistic Regression model.
4. **`predict_on_test_data`**: Predicts the class labels for the test data.
5. **`predict_prob_on_test_data`**: Predicts the class probabilities for the test data.
6. **`get_matrices`**: Evaluates the model's performance using metrics such as accuracy, precision, recall, and log loss.

## File Structure

- **`ml_pipeline.py`**: Contains the DAG definition and task logic.
- **`requirements.txt`**: Lists the Python dependencies.
- **`final_df.csv`**: Processed dataset file (generated during execution).
- **`model.pkl`**: Trained Logistic Regression model (generated during execution).
- **`x_train.npy`, `x_test.npy`, `y_train.npy`, `y_test.npy`, `y_pred.npy`, `y_pred_prob.npy`**: Intermediate files for train-test split and predictions.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ml-pipeline.git
   cd ml-pipeline
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up Apache Airflow:
   ```bash
   export AIRFLOW_HOME=~/airflow
   airflow db init
   airflow users create \
       --username admin \
       --firstname Admin \
       --lastname User \
       --role Admin \
       --email admin@example.com
   ```

4. Add the DAG file to your Airflow DAGs folder:
   ```bash
   cp ml_pipeline.py $AIRFLOW_HOME/dags/
   ```

5. Start the Airflow scheduler and web server:
   ```bash
   airflow scheduler &
   airflow webserver &
   ```

6. Access the Airflow UI at `http://localhost:8080` and enable the `ml_pipeline` DAG.

## Requirements

- pandas
- numpy
- scikit-learn
- pickle
- apache-airflow

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Airflow web server and scheduler as described in the installation steps.
2. Enable the `ml_pipeline` DAG from the Airflow UI.
3. Monitor the progress of the tasks in the UI.
4. Check the generated files (`model.pkl`, `final_df.csv`, etc.) for results.

## Model Metrics

The `get_matrices` task evaluates the model's performance and prints the following metrics:

- **Accuracy**
- **Precision**
- **Recall**
- **Log Loss**
- **Classification Report**

## Dataset

The pipeline uses the Iris dataset, which is downloaded from the following URL:
[https://raw.githubusercontent.com/TripathiAshutosh/dataset/main/iris.csv](https://raw.githubusercontent.com/TripathiAshutosh/dataset/main/iris.csv)

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improving this pipeline.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

