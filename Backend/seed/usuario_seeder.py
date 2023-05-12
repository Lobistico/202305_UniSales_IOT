import os
import sys
core_path = os.path.abspath("./")
sys.path.append(core_path)

from typing import Generator
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from models.usuario_model import UsuarioModel
from core.security import gerar_hash_senha
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.database import engine 
Session: AsyncSession = async_sessionmaker(bind=engine)

novo_usuario: UsuarioModel = UsuarioModel(
        nome='root',
        email='root@hotmail.com', 
        senha=gerar_hash_senha('root'), 
        criado_em=str(datetime.now()), 
        atualizado_em=str(datetime.now())
        )

async def criar_usuario():
    session: AsyncSession = Session()
    async with session as conn:
        try:
            conn.add(novo_usuario)
            await conn.commit()
        finally:
            await session.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(criar_usuario())


