FROM apache/airflow:2.7.3

RUN pip install --upgrade pip

COPY requirements.txt /opt/airflow/

USER airflow

RUN pip install --no-cache-dir -r requirements.txt
