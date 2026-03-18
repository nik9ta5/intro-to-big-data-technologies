from pyspark.sql import functions as F

from tools import argument_parsing
from spark_session import spark_session_create


if __name__ == "__main__":
    
    args = argument_parsing()
    
    db_name = args.db_name
    table_name = args.table_name

    spark = spark_session_create(args.root_name, args.root_password, args.bucket_name)

    print('==============')
    print('connection successful')

    
    result_query = spark.sql(f"SELECT * FROM local_catalog.{db_name}.{table_name}").show(10, vertical=True)
    print(result_query)


    print('done')
    print('==============')