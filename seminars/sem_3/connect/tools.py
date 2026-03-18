import argparse

def argument_parsing() -> dict:
    parser = argparse.ArgumentParser(description="Connect to MinIO")
    # Обязательные аргументы (парсит в последовательно, в порядке передачи)
    parser.add_argument("root_name", help="username for user root minio")
    parser.add_argument("root_password", help="password for user root minio")
    parser.add_argument("bucket_name", help="bucket for save data")
    parser.add_argument("db_name", help="name for db")
    parser.add_argument("table_name", help="table_name for save data")
    return parser.parse_args()