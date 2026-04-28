from airflow.decorators import dag, task
from datetime import datetime, timedelta

from tools.arg_parse import get_airflow_connection, get_airflow_parameters, load_dag_config
from tools.spark_session_create import spark_session_create
from tools.spark_transforms import raw_data_preprocess_pipeline


@dag(
    dag_id='simple_dag',          
    default_args={
    'owner': 'userairflow',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
    'start_date': datetime(2026, 4, 22),
},
    schedule=None,                 
    catchup=False,                  
    tags=['test', 'connection', 'variables'],   
    description='Create first simple DAG',
)
def read_connection_variables_pipeline(): 

    # ========================= Полное описание всего pipeline ========================= 

    @task(task_id="simple_print")
    def simple_print():
        print("\n=========\nHello, first task in DAG\n=========\n")

        cfg = load_dag_config("configs/config.yaml")
        print(cfg)


    # ============= Тестовая задача для парсинга connection и variables =============
    @task(task_id='get_connection')
    def get_connection_variables():
        connection_params = get_airflow_connection("test_conn1")
        variables_params = get_airflow_parameters()

        print(connection_params)
        print(variables_params)

    
    @task(task_id="create_conn_minio")
    def create_conn_minio():
        cfg = load_dag_config("configs/config.yaml")

        spark = spark_session_create(
            cfg["spark_connect"]["root_user"],
            cfg["spark_connect"]["root_password"],
            cfg["spark_connect"]["buck_name"],
            cfg["spark_connect"]["srotage_url"],
            cfg["spark_connect"]["spark_cache_dir"],
        )

        raw_data_preprocess_pipeline(
            spark,
            cfg["spark_connect"]["db_name"],
            cfg["spark_connect"]["table_name"],
            cfg["path2raw_data"]
        )
        


    # ========================= Вызов задач ========================= 
    result_task1 = simple_print()
    result_task2 = get_connection_variables()
    resutl_task3 = create_conn_minio()

    # simple_print >> get_connection_variables >> create_conn_minio
    result_task1 >> result_task2 >> resutl_task3


# ==================== объект DAG ====================
simple_dag = read_connection_variables_pipeline()