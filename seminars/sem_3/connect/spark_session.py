from pyspark.sql import SparkSession

def spark_session_create(root_name, root_password, bucket_name):
    PACKAGES = ",".join([
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262",
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0",
        "org.apache.iceberg:iceberg-aws-bundle:1.5.0"
    ])

    # === create spark session ===  
    spark = (
        SparkSession.builder 
        .appName("Lakehouse create")

        .config("spark.driver.memory", "2g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.shuffle.partitions", "10")
        
        # === директория для временных данных spark ===
        .config("spark.local.dir", "./spark_local_cache")

        # === зависимости ===
        .config("spark.jars.packages", PACKAGES)
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")

        # === Настройка Iceberg Каталога ===
        .config("spark.sql.catalog.local_catalog", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.local_catalog.type", "hadoop") # rest/jdbc/hive
        .config("spark.sql.catalog.local_catalog.warehouse", f"s3a://{bucket_name}/warehouse/")

        .config("spark.sql.catalog.local_catalog.s3.access-key-id", root_name)
        .config("spark.sql.catalog.local_catalog.s3.secret-access-key", root_password)
        .config("spark.sql.catalog.local_catalog.s3.path-style-access", "true")

        # === нативный IO Iceberg для S3 ===
        .config("spark.sql.catalog.local_catalog.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
        .config("spark.sql.catalog.local_catalog.s3.endpoint", "http://127.0.0.1:9050")

        # === настройка hadoop для чтения ===
        .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9050")
        .config("spark.hadoop.fs.s3a.access.key", root_name)
        .config("spark.hadoop.fs.s3a.secret.key", root_password)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
        
        # === регион клиента ===
        .config("spark.sql.catalog.local_catalog.client.region", "us-east-1")

        # === формат передачи данных arrow ===
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")

        .getOrCreate()
    )   
    
    return spark