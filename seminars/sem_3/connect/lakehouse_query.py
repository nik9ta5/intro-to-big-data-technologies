from pyspark.sql import functions as F

from tools import argument_parsing
from spark_session import spark_session_create
from pack1.simpel import fucn1


if __name__ == "__main__":
    
    args = argument_parsing()
    
    db_name = args.db_name
    table_name = args.table_name

    spark = spark_session_create(args.root_name, args.root_password, args.bucket_name)

    print('==============')
    print('connection successful')

    
    result_query = spark.sql(f"""
        SELECT request_date, COUNT(*) FROM local_catalog.{db_name}.{table_name}
        GROUP BY(request_date)
        ORDER BY (request_date)
    """).show(90)
    
    print(result_query)


    print('done')
    print('==============')