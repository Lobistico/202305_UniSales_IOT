from core.configs import settings
from core.database import engine

async def create_tables():
    import models.__all_models
    async with engine.begin() as conn:
            print('Criando as tabelas no banco de dados...')
            await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
            await conn.run_sync(settings.DBBaseModel.metadata.create_all)
            print('Tabelas criadas')
if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())