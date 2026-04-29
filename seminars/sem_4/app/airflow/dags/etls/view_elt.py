from pathlib import Path
from datetime import datetime

from pyspark.sql import functions as F


def view_stats_elt(
    spark, 
    db_name: str,
    table_name: str,
    path2file_write: Path = None,
    path2data: str = None
    ) -> None:

    time_now = datetime.now()
    time_now_human_str = str(time_now.strftime("%H:%M:%S, %d-%m-%Y"))

    print("========================")

    result_query = spark.sql(f"""
        SELECT request_date, COUNT(*) FROM local_catalog.{db_name}.{table_name}
        GROUP BY(request_date)
        ORDER BY (request_date)
    """)
    
    row_datas = result_query.collect()

    if path2file_write:
        with open(path2file_write, "a", encoding="utf-8") as file:
            file.writelines(f"\n === {time_now_human_str} ===\n")

            for row in row_datas:
                file.write(f"{row[0]}: {row[1]}\n")

    print("========================")
    
    return None