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




router = APIRouter(dependencies=[Depends(get_current_user)])
routerLogin = APIRouter()

@router.get('/me', response_model=UsuarioSchemaBase)
async def me(usuario = Depends(get_current_user)):
    return usuario
    
@routerLogin.post('/login')
async def autentica_user(OAuth2PasswordRequestForm: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == OAuth2PasswordRequestForm.username)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if(usuario and (comparar_senha(OAuth2PasswordRequestForm.password, usuario.senha))):
            token = criar_acess_token(str(usuario.id))
            return {
                "access_token": token,
                "token_type": "bearer"
            }
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorretos")    

            
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(nome = Form(...), email = Form(...), senha = Form(...),db: AsyncSession = Depends(get_session), file: UploadFile = File(..., media_type='image/jpeg')):
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    dir = os.path.abspath('./assets/image/')
    
    with open(f"{dir}{file.filename}", "wb") as f:
        f.write(contents)

    novo_usuario: UsuarioModel = UsuarioModel(
        nome=nome, 
        email=email,
        imagem= f"{dir}{file.filename}", 
        senha=gerar_hash_senha(senha), 
        criado_em = str(datetime.now()), 
        atualizado_em = str(datetime.now()))
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Não foi possivel criar novo usuário')
        
        
@router.get('/', response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session), usuarioLogado = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        return usuarios
    
@router.get('/{id}', response_model=UsuarioSchemaTarefa)
async def get_usuario(id: int, db: AsyncSession = Depends(get_session), usuarioLogado = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()
        if usuario:
            return usuario
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
        
@router.delete('/{id}', status_code= status.HTTP_204_NO_CONTENT)
async def delete_usuario(id: int, db: AsyncSession = Depends(get_session), usuarioLogado = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()
        if usuario:
            await session.delete(usuario)
            await session.commit()
            Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)
        
@router.put('/{id}' ,status_code= status.HTTP_202_ACCEPTED, response_model=UsuarioSchemaBase)
async def put_usuario(id: int, nome = Form(...), email = Form(...), senha = Form(...) , file: UploadFile = File(..., media_type='image/jpeg'), db: AsyncSession = Depends(get_session), usuarioLogado = Depends(get_current_user)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == id)
        result = await session.execute(query)
        usuario_update: UsuarioSchemaCreate = result.scalars().unique().one_or_none()

        if os.path.exists(usuario_update.imagem):
            os.remove(usuario_update.imagem)
            
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()
        dir = os.path.abspath('./assets/image/')
        
        with open(f"{dir}{file.filename}", "wb") as f:
            f.write(contents)

        if usuario_update:
            usuario_update.nome = nome
            usuario_update.email = email 
            usuario_update.senha = senha
            usuario_update.imagem = f"{dir}{file.filename}"
            usuario_update.atualizado_em = str(datetime.now())
            await session.commit()
            return usuario_update
        else:
            raise HTTPException(detail='Usuário não encontrado',
                                status_code=status.HTTP_404_NOT_FOUND)



@router.post("/upload")
async def create_upload_file(file: UploadFile = File(...)):
 
    file.filename = f"{uuid.uuid4()}.jpg"
    contents = await file.read()
    dir = os.path.abspath('./assets/image/')
    
    with open(f"{dir}{file.filename}", "wb") as f:
        f.write(contents)
    return {"filename": file.filename}
 
