from fastapi import APIRouter
from api.v1.endpoints import usuario, plantacao

api_router = APIRouter()
api_router.include_router(usuario.router, prefix='/usuarios', tags=['usuarios'])
api_router.include_router(plantacao.router, prefix='/plantacao', tags=['plantacao'])
api_router.include_router(usuario.routerLogin, prefix='/usuarios', tags=['usuarios'])




