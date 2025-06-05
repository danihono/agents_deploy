
from pydantic import BaseModel

class EnvVar(BaseModel):
    name: str
    description: str = ""
    required: bool = False
