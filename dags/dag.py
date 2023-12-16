from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

sys_path = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(sys_path)) # Adding the entire directory to path

from etl.extract import generate_data
from etl.s3 import s3_pipeline


default_args = {
    'owner': 'Abdulkaabeer',
    'start_date': datetime(2023, 12, 2)    
}


with DAG(
    dag_id='elt_s3_redshift',
    description='Faker ETL',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    faker_extract = PythonOperator(
        task_id='faker_extract',
        python_callable=generate_data
    )

    s3_upload = PythonOperator(
        task_id='s3_upload',
        python_callable = s3_pipeline
        
    )



faker_extract >> s3_upload