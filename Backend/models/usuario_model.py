from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.configs import settings
from sqlalchemy.orm import relationship
import datetime

class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios' 
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(255), nullable= True)
    imagem: str = Column(String(255), nullable= True)
    email: str = Column(String(255), nullable=False, unique=True)
    senha: str = Column(String(255), nullable= False)
    criado_em: str = Column(DateTime, nullable= True)
    atualizado_em: str = Column(DateTime, nullable= True)
