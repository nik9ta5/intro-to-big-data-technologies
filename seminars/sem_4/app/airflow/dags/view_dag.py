import os
from pathlib import Path

from airflow.decorators import dag, task
from datetime import datetime, timedelta

from tools.arg_parse import load_dag_config
from tools.spark_session_create import spark_session_create
from etls.view_elt import view_stats_elt

@dag(
    dag_id='view_elt',          
    default_args={
    'owner': 'userairflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=2),
    'start_date': datetime(2026, 4, 29),
},
    # schedule=None,
    schedule=timedelta(minutes=2), # выполнять каждые 2 минут                 
    catchup=False,                  
    tags=['test', 'load', 'elt'],   
    description='Create ELT DAG',
)
def view_stats_data(): 

    @task(task_id="elt_view_data")
    def elt_view_data():
        
        # === read config file ===
        config = load_dag_config("./configs/config.yaml")
        
        # === create spart session ===
        spark = spark_session_create(
            root_name=config['minio']['root_user'],
            root_password=config['minio']['root_password'],
            bucket_name=config['minio']['lakehouse_bucket'],
            srotage_url=config['minio']['srotage_url'],
            driver_memory=config['spark_params']['driver_memory'],
            executor_memory=config['spark_params']['executor_memory'],
            shuffle_partitions=config['spark_params']['shuffle_partitions'],
            spark_temp_folder=config['spark_params']['spark_temp_folder'],
            spark_cache_folder=config['spark_params']['spark_cache_folder']
        )

        path2write_file = Path("./outputs/out.txt")
        # ==========================================
        os.makedirs("./outputs", exist_ok=True)
        if path2write_file.is_file():
            pass
        else:
            with open(path2write_file, "w", encoding="utf-8") as file:
                file.writelines("--- init ---")
        # ==========================================

        try:
            view_stats_elt(
                spark,
                config['spark_connect']['db_name'],
                config['spark_connect']['table_name'],
                path2write_file
            )
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            # === spark stop ===
            spark.stop()


        print("done task")

    # === Tasks ===

    task_first = elt_view_data()

    task_first

simple1 = view_stats_data()