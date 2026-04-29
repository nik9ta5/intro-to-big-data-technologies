from airflow.decorators import dag, task
from datetime import datetime, timedelta

from tools.arg_parse import load_dag_config
from tools.spark_session_create import spark_session_create

@dag(
    dag_id='simple1',          
    default_args={
    'owner': 'userairflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2026, 4, 29),
},
    schedule=None,                 
    catchup=False,                  
    tags=['test'],   
    description='Create second simple DAG',
)
def read_connection_variables_pipeline(): 

    @task(task_id="print1")
    def simple_print():
        print("\n=========\nHello, first task in DAG\n=========\n")

    @task(task_id="load_cfg")
    def load_config():
        config = load_dag_config("./configs/config.yaml")
        print(config)

    @task(task_id="spark_session_create_test")
    def spark_session_create_test():
        config = load_dag_config("./configs/config.yaml")
        
        spark = spark_session_create(
            root_name=config['minio']['root_user'],
            root_password=config['minio']['root_password'],
            bucket_name=config['minio']['lakehouse_bucket'],
            srotage_url=config['minio']['srotage_url'],
            driver_memory=config['spark_params']['driver_memory'],
            executor_memory=config['spark_params']['executor_memory'],
            shuffle_partitions=config['spark_params']['shuffle_partitions'],
            spark_cache_folder=config['spark_params']['spark_cache_dir']
        )

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
            spark_cache_folder=config['spark_params']['spark_cache_dir']
        )

        df = spark.read.parquet(f"s3a://{config['minio']['raw_data_bucket']}/{config['raw_data_first_part']}")
    
        print(df.count())

    result = simple_print()
    result2 = load_config()
    result3 = spark_session_create_test()
    result4 = spark_count_task()

    result2 >> result4

simple1 = read_connection_variables_pipeline()