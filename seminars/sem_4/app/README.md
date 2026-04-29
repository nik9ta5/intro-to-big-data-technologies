Структура проекта
* `airflow/` - директория для работы с airflow
  - `airflow/dags/` - директория, в которой будут находиться соответствующие скрипты с DAG-ами
  - `airflow/logs/`
  - `airflow/spark_local_cache/` - папка с кэшем pyspark
  - `airflow/spark_local_temp/` - папка с временными файлами pyspark
  - `airflow/Dockerfile`
  - `airflow/requirements.txt`
* `postgres/` - директория для работы с postgres
  - `postgres/postgres_data/` - папка с данными postgres
  - `postgres/Dockerfile`
* `storage_lakehouse/` - директория для работы с хранилищем MinIO
  - `storage_lakehouse/storage_data/`
  - `storage_lakehouse/Dockerfile`
* `.env` - файл с секретами (пример файла: `example.env`)
* `docker-compose.yml` 
* `.gitignore`
* `README.md` 