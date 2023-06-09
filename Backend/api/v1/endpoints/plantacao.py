import api.v1.endpoints
import fastapi.security
import pydantic
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response, File, UploadFile, Form, Request
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from core.deps import get_session
from core.security import gerar_hash_senha, comparar_senha
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from schemas.usuario_schema import * 
from schemas.plantacao import * 
from core.auth import criar_acess_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import os
from core.configs import settings
from core.database import engine
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client, os, time


BUCKET="irrigation"
BUCKET_AREA_REGADA="area_regada"

client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)
router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post('/regar', status_code=status.HTTP_201_CREATED)
async def post_usuario(plantancao: Plantacao):
    try:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        point = Point("area_regada").tag("regado", plantancao.regado).field("nome", plantancao.sensor)
        write_api.write(bucket=BUCKET_AREA_REGADA, org=settings.INFLUXDB_ORG, record=point)
        return f'Area do sensor {plantancao.sensor} esta sendo regada!'
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Houve um erro interno')
    
@router.get('/areas_regadas/{sensor}')
async def getAll(request: Request, sensor:str):
    query = f'from(bucket: "area_regada") |> range(start: -24h) |> filter(fn: (r) => r._value == "{sensor}")'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)
    data = []

    for table in result:
        for record in table.records:
            data.append(record.values)
    return data

@router.get('/relatorio/{sensor}')
async def getAll(request: Request, sensor:str):
    query = f'from(bucket: "irrigation") |> range(start: -24h) |> filter(fn: (r) => r._measurement == "{sensor}")'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)
    data = []

    for table in result:
        for record in table.records:
            data.append(record.values)
    return data



@router.get("/{sensor}")
async def getBySensor(request: Request, sensor: str):
    query = f'from(bucket: "irrigation") |> range(start: -1d) |> filter(fn: (r) => r._measurement == "{sensor}" and (r._field == "temperatura" or r._field == "umidade"))'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)
    data = []

    for table in result:
        table.records.sort(key=lambda r: r.get_time(), reverse=True)
        if len(table.records) > 0:
            data.append(table.records[0].values)

    return data



# @router.put('/{id}')
# async def update():
#     return 'plantacao altera por {id}'


# @router.delete('/{id}')
# async def delete():
#     return 'plantacao delete por id'




    

