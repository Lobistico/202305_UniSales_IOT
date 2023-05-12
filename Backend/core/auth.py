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

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não Autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        usuario_id: str = payload.get('sub')
        async with db as session:
            query = select(UsuarioModel).filter(UsuarioModel.id == int(usuario_id))
            result = await session.execute(query)
            usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()
            if usuario:
                return usuario
            else:
                raise credentials_exception
    except JWTError:
        raise credentials_exception
    

            

    
        








