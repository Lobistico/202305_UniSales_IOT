import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    DB_URL: str = 'mysql+asyncmy://root:root@localhost/seed?charset=utf8mb4'
    DBBaseModel = declarative_base()

    os.environ['INFLUXDB_TOKEN'] = 'j7kUqCye2TUYwX7IsjE4Yx718l0FNbBAwKyuJ32G2es'

    token = os.environ.get("INFLUXDB_TOKEN")
    org = "my-org"
    url = "http://localhost:8086"

    write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)



    class Config:
        case_sensitive: True


settings = Settings()