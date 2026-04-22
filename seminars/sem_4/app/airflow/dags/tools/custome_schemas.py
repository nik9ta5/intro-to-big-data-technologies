from pydantic import BaseModel, Field

class MinioConfig(BaseModel):
    bucket_raw: str
    bucket_processed: str

class SparkConfig(BaseModel):
    executor_memory: str = "1g"
    parallelism: int

class FullConfig(BaseModel):
    project_name: str
    minio: MinioConfig
    spark_params: SparkConfig