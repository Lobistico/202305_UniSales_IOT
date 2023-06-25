import api.v1.endpoints
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.deps import get_session
from models.usuario_model import UsuarioModel
import sqlalchemy.ext.asyncio
from sqlalchemy.future import select
from core.deps import get_session
from schemas.usuario_schema import *
from jose.exceptions import JWTError
from core.configs import settings

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import influxdb_client, os, time

bucket="Usuarios"
client = InfluxDBClient(url=settings.INFLUXDB_URL, token=settings.INFLUXDB_TOKEN, org=settings.INFLUXDB_ORG)

SECRET_KEY: str = 'j7kUqCye2TUYwX7IsjE4Yx718l0FNbBAwKyuJ32G2es'
ALGORITH: str = 'HS256'
EXPIRES_IN_MIN = 60*24*7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/usuarios/login")

def criar_acess_token(usuario_id: str):
    expiracao = str(datetime.utcnow() + timedelta(EXPIRES_IN_MIN))
    payload = {
        'sub': usuario_id,
        'ext': expiracao
        }
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITH)
    return token_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não Autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        usuario_id: str = payload.get('sub')

        query = 'from(bucket: "Usuarios") |> range(start: -1d) |> limit(n: 10)'
        result = client.query_api().query(org=settings.INFLUXDB_ORG, query=query)

        data = []        
        for table in result:
            for record in table.records:
                if record.values["email"] == usuario_id:
                    data.append(record.values)
        return data
        
    except JWTError:
        raise credentials_exception
    

            

    
        








