import pandas as pd
import fitz # Ее нет в изначально образе, поэтому придется доставлять отдельно (pip install PyMuPDF)
from airflow.decorators import dag, task
from datetime import datetime, timedelta

from tools.arg_parse import load_dag_config
from tools.spark_session_create import spark_session_create


def extract_text_from_pdf(pdf_bytes: pd.Series) -> pd.Series:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = "\n\n".join(page.get_text("text") for page in doc)
        doc.close()
        return text.strip()
    except Exception as e:
        return f"ERROR extracting text: {str(e)}"
    

@dag(
    dag_id='raw_file_load', default_args={
        'owner': 'userairflow',
        'retries': 2,
        'retry_delay': timedelta(minutes=1),
        'start_date': datetime(2026, 4, 22),
    },
    schedule=None, catchup=False, tags=['text', 'load'], description='load files',
)
def raw_file_load(): 
    @task(task_id="load_files")
    def load_files():
        cfg = load_dag_config("configs/config.yml")
        spark = spark_session_create(
            cfg["minio"]["root_user"],
            cfg["minio"]["root_password"],
            cfg["minio"]["raw_data_bucket"],
            cfg["minio"]["srotage_url"],
            cfg["spark_params"]["driver_memory"],
            cfg["spark_params"]["executor_memory"],
            cfg["spark_params"]["shuffle_partitions"],
            cfg["spark_params"]["spark_temp_folder"],
            cfg["spark_params"]["spark_cache_folder"]
        )
        
        bucket = "raw-docs"
        prefix = "docs-part1"

        df_binary = (spark.read.format("binaryFile")
             .option("pathGlobFilter", "*.pdf")    
             .option("recursiveFileLookup", "true")       
             .load(f"s3a://{bucket}/{prefix}"))

        df_binary.select(
            "path", 
            "length", 
            "modificationTime"
        ).show(truncate=False)

        print(df_binary.count())

        collects = df_binary.collect()
        for item in collects:
            all_text = extract_text_from_pdf(item['content'])
            print(all_text)
            break

        # === end ===

    task_files_load = load_files()

    task_files_load

simple_dag = raw_file_load()