import datetime
from typing import Optional, List
from pydantic import BaseModel as SCBaseModel, EmailStr
from datetime import datetime

class TarefaSchema(SCBaseModel):
    id: Optional[int]
    usuario_id: Optional[int]
    nome: str
    descricao: str
    concluido: bool
    criado_em: Optional[datetime]
    atualizado_em: Optional[datetime]

    class Config:
        orm_mode = True