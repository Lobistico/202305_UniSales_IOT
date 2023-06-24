import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from pydantic import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    DB_URL: str = 'mysql+asyncmy://root:root@localhost/seed?charset=utf8mb4'
    BUCKET: str ="Usuarios"
    DBBaseModel: str = declarative_base()

    INFLUXDB_TOKEN: str = "167x85pD7ILjp39izsESGQiffxb3MXrEKP8jcay_r_uullGq47QQ7DebXNgDQ0pQG3hP8ZQlhcDB66vJMv_OZg=="
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_ORG: str = "my-org"
    



    class Config:
        case_sensitive: True


settings = Settings()