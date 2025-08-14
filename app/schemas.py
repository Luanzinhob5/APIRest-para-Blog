from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    id: int
    titulo: str
    descricao: str
    conteudo: str

    class Config:
        from_attributes = True

class PostCriarSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=150)
    descricao: str = Field(..., max_length=300)
    conteudo: str = Field(..., max_length=2000)
