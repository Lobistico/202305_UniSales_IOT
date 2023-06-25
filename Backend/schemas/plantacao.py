import datetime
from typing import Optional, List
from pydantic import BaseModel as SCBaseModel, EmailStr
from datetime import datetime

class Plantacao(SCBaseModel):
    id: Optional[int]
    regado: bool
    sensor: str

    class Config:
        orm_mode = True