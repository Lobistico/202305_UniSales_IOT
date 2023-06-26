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

    INFLUXDB_TOKEN: str = "Kt3E1sjNuZ6nCsbDAv6v7kQYmd_bCuzwysNO59WTTFe6bZOaglavqyCeLh9wU2BKfALDauOynwdPHyLPPYsb1Q=="
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_ORG: str = "my-org"
    



    class Config:
        case_sensitive: True


settings = Settings()