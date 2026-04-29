from airflow.decorators import dag, task
from datetime import datetime, timedelta

from tools.arg_parse import load_dag_config
from tools.spark_session_create import spark_session_create
from etls.load_storage import load_storage


@dag(
    dag_id='load_elt',          
    default_args={
    'owner': 'userairflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2026, 4, 29),
},
    schedule=None,                 
    catchup=False,                  
    tags=['test', 'load', 'elt'],   
    description='Create ELT DAG',
)
def read_connection_variables_pipeline(): 


    @task(task_id="spark_count_task")
    def spark_count_task():
        config = load_dag_config("./configs/config.yaml")
        
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

        df = spark.read.parquet(f"s3a://{config['minio']['raw_data_bucket']}/{config['raw_data_first_part']}")
    
        print(df.count())


    @task(task_id="elt_load_storage_data_taks")
    def elt_load_storage_data_taks():
        
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

        # === call load data function ===
        load_storage(
            spark,
            config['spark_connect']['db_name'],
            config['spark_connect']['table_name'],
            f"s3a://{config['minio']['raw_data_bucket']}/{config['raw_data_first_part']}",
            is_create_or_replace=True,
            partittion_by="request_date"
        )

        print("done task")

    # === Tasks ===

    result = spark_count_task()
    task_load_data = elt_load_storage_data_taks()


simple1 = read_connection_variables_pipeline()