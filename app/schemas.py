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


class PostAtualizarSchema(BaseModel):
    titulo: str = Field(None, min_length=3, max_length=150)
    descricao: str = Field(None, min_length=3, max_length=300)
    conteudo: str = Field(None, min_length=3, max_length=2000)

class UsuarioSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    password: str = Field(..., min_length=6)

class TokenSchema(BaseModel):
    access_token: str