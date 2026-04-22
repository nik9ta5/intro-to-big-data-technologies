import argparse

import yaml
from pathlib import Path
from tools.custome_schemas import FullConfig

from airflow.models import Variable
from airflow.hooks.base import BaseHook


def argument_parsing() -> dict:
    parser = argparse.ArgumentParser(description="Connect to MinIO")

    parser.add_argument("root_name", help="username for user root minio")
    parser.add_argument("root_password", help="password for user root minio")
    parser.add_argument("bucket_name", help="bucket for save data")
    parser.add_argument("db_name", help="name for db")
    parser.add_argument("table_name", help="table_name for save data")

    return parser.parse_args()

def get_airflow_connection(conn_id: str):
    """function for get connection airflow"""
    conn = BaseHook.get_connection(conn_id)
    print(f"\n=== Conn ===\n{conn}\n======\n")
    return {
        "login" : conn.login,
        "password" : conn.password,
        "endpoint_url" : conn.extra_dejson.get('endpoint_url')
    }

def get_airflow_parameters():
    return {
        "root_username" : Variable.get("root_username"),
        "root_password" : Variable.get("root_password"),
        "endpoint_url" : Variable.get("endpoint_url")
    }

def load_dag_config(filename: str) -> FullConfig:
    config_path = Path(__file__).parent.parent / filename
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    # return FullConfig(**raw_config)
    return raw_config