from pydantic import BaseModel


class ModifyRequest(BaseModel):
    location: str
