import api.v1.endpoints
import fastapi.security
import pydantic
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import  AsyncSession
from sqlalchemy.future import select
from models.usuario_model import UsuarioModel
from core.deps import get_session
from core.security import gerar_hash_senha, comparar_senha
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from schemas.usuario_schema import * 
from core.auth import criar_acess_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
import uuid
import os
from core.configs import settings
from core.database import engine
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client, os, time


BUCKET="Usuarios"
client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)
router = APIRouter(dependencies=[Depends(get_current_user)])
routerLogin = APIRouter()

@routerLogin.post('/signup', status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate):
    
    query = 'from(bucket: "Usuarios") |> range(start: -1d) |> limit(n: 10)'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)
    
    data = []
    for table in result:
        for record in table.records:
            if record.values["email"] == usuario.email:
                data.append(record.values)
            
    if data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Já existe um usuario com este email')
    else:   
        try:
            
            dir = os.path.abspath(f"./assets/image/{usuario.imagem}")
            write_api = client.write_api(write_options=SYNCHRONOUS)
            point = Point("usuário").tag("email", usuario.email).tag("nome", usuario.nome).tag("imagem", dir).field("senha", gerar_hash_senha(usuario.senha))
            write_api.write(bucket=BUCKET, org=settings.INFLUXDB_ORG, record=point)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Não foi possivel criar novo usuário')
            
    return usuario


@router.get('/me')
async def me(usuario = Depends(get_current_user)):
    return usuario
    

@routerLogin.post('/login')
async def autentica_user(OAuth2PasswordRequestForm: OAuth2PasswordRequestForm = Depends()):
    query = 'from(bucket: "Usuarios") |> range(start: -1d) |> limit(n: 10)'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)
    
    data = []
    for table in result:
        for record in table.records:
            if record.values["email"] == OAuth2PasswordRequestForm.username and comparar_senha(OAuth2PasswordRequestForm.password, record.values["_value"]):
                data.append(record.values)
    if data:
        token = criar_acess_token(str(record.values["email"]))
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorretos") 

@router.get('/')
async def get_usuarios(db: AsyncSession = Depends(get_session), usuarioLogado = Depends(get_current_user)):
    query = 'from(bucket: "Usuarios") |> range(start: -1d) |> limit(n: 10)'
    result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)

    data = []
    for table in result:
        for record in table.records:
            data.append(record.values)
    return data


    

