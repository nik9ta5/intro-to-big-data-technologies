from pyspark.sql import functions as F

def load_storage(
    spark, 
    db_name: str,
    table_name: str,
    path2raw_data: str,
    is_create_or_replace: bool = False,
    partittion_by: str = "request_date",
    ):

    # Создаем датафрейм
    df = spark.read.parquet(path2raw_data)

    print("========================")

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
    if is_create_or_replace:
        (
            df_filer_one
            .writeTo(f"local_catalog.{db_name}.{table_name}")
            .tableProperty("write.format.default", "parquet")
            .tableProperty("write.target-file-size-bytes", "134217728") # 128 MB
            .partitionedBy(F.col(partittion_by))
            .createOrReplace()
        )
        print("done create and write")
    else:
        (
            df_filer_one
            .writeTo(f"local_catalog.{db_name}.{table_name}")
            .tableProperty("write.format.default", "parquet")
            .tableProperty("write.target-file-size-bytes", "134217728") # 128 MB
            .partitionedBy(F.col(partittion_by))
            .overwritePartitions() 
            # .append()
        )
        print("done overwritePartitions")
    
    print("========================")