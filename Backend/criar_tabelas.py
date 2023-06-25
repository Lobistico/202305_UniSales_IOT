from core.configs import settings
from core.database import engine
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client, os, time

async def create_tables():
    import models.__all_models
    async with engine.begin() as conn:
            print('Criando as tabelas no banco de dados...')
            await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
            await conn.run_sync(settings.DBBaseModel.metadata.create_all)
            print('Tabelas criadas')


def testeInfluxDb():
    import os
    bucket="Usuarios"

    # Criação do cliente InfluxDB
    client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)

    # Criação do WriteApi
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Dados do usuário
    email = "root@root.com"
    senha = "$2b$12$O4fqRQV.jT/oBD6WagmJa.PqYro8L/LYwy4otTz506UPUXiysGtgC"

    # Criação do ponto de dados
    point = Point("usuário").tag("email", email).field("senha", senha)

    # Gravação do ponto de dados no InfluxDB
    write_api.write(bucket=bucket, org=settings.INFLUXDB_ORG, record=point)




if __name__ == '__main__':
    import asyncio
    testeInfluxDb()
    # asyncio.run(create_tables())