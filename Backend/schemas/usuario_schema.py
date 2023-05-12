import datetime
from typing import Optional, List
from pydantic import BaseModel as SCBaseModel, EmailStr
from datetime import datetime
from schemas.tarefa_schema import TarefaSchema

class UsuarioSchemaBase(SCBaseModel):
    id: Optional[int]
    nome: str
    email: str
    imagem: Optional[str]
    criado_em: Optional[datetime]
    atualizado_em: Optional[datetime]

    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

    class Config:
        orm_mode = True

class UsuarioSchemaToken(SCBaseModel):
    usuario: UsuarioSchemaBase
    acess_token: str

class UsuarioSchemaTarefa(UsuarioSchemaBase):
    tarefas: List[TarefaSchema]
    
    
    


