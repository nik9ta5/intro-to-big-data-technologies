from tqdm import tqdm

from pyspark.sql import functions as F

from tools import argument_parsing
from spark_session import spark_session_create



if __name__ == "__main__":

    # Парсим аргументы
    args = argument_parsing()

    # Создаем spark сессию
    spark = spark_session_create(args.root_name, args.root_password, args.bucket_name) 
    

    # Создаем датафрейм к источнику данных
    df = spark.read.parquet("s3a://raw-data/raw2-data/*.parquet")
    

    print("========================")
    print("connect successful")

    # Выполняем фильтрацию
    df_filer_one = df.filter(
        (df.trip_miles > 0) & 
        (df.trip_time > 0)  & 
        (df.driver_pay > 0) & 
        (df.tips >= 0)
    )

    # Преобразуем колонки с датой и временем к желаемому типу
    df_filer_one = (
        df_filer_one
        .withColumn("request_datetime", F.to_timestamp(F.col("request_datetime"), "yyyy-MM-dd HH:mm:ss"))
        .withColumn("on_scene_datetime", F.to_timestamp(F.col("on_scene_datetime"), "yyyy-MM-dd HH:mm:ss"))
        .withColumn("pickup_datetime", F.to_timestamp(F.col("pickup_datetime"), "yyyy-MM-dd HH:mm:ss"))
        .withColumn("dropoff_datetime", F.to_timestamp(F.col("dropoff_datetime"), "yyyy-MM-dd HH:mm:ss"))
        # Только дата из даты обращения
        .withColumn("request_date", F.to_date(F.col("request_datetime")))
        # Полная цена поездки
        .withColumn("total_price", F.col("base_passenger_fare") + F.col("tolls") + F.col("bcf") + F.col("sales_tax") + F.col("congestion_surcharge") + F.col("airport_fee"))
    )

    # Заполняем пропуски в колонке originating_base_num
    df_filer_one = df_filer_one.fillna({
        "originating_base_num":"UNKWN"   
    }) 

    # Признаки, которые сохраним для дальнейшей работы
    final_columns = [
        "request_datetime",
        "on_scene_datetime",
        "pickup_datetime",
        "dropoff_datetime",
        "PULocationID",
        "DOLocationID",
        "trip_miles",
        "total_price",
        "tips",
        "driver_pay",
        "shared_request_flag",
        "shared_match_flag",
        "request_date"
    ]

    # Выбираем колонки
    df_filer_one = df_filer_one.select(*final_columns)
        
    print("writing data to Iceberg table...")
    
    # Выполяем запись в хранилище
    (
        df_filer_one
        .writeTo(f"local_catalog.{args.db_name}.{args.table_name}")
        .tableProperty("write.format.default", "parquet")
        .tableProperty("write.target-file-size-bytes", "134217728") # 128 MB
        .partitionedBy(F.col("request_date"))
        # .overwritePartitions()
        .createOrReplace()
    )

    print("done")
    print("========================")