from pydantic import BaseModel, Field
from typing import Optional

class PostCriarSchema(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=150, description="O titulo do post")
    descricao: str = Field(...,max_length=300, description="A Descricao do post")
    conteudo: str = Field(..., max_length=20000, description="O Conteudo completo do Post")

class PostAlterarSchema(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=150)
    descricao: Optional[str] = Field(None, max_length=300)
    conteudo: Optional[str] = Field(None, max_length=20000)


class UsuarioCriarSchema(BaseModel):
    nome: str = Field(..., min_length=4, max_length=18, description="O nome do usuario")
    email: str = Field(..., min_length=8, max_length=40, description="O email do usuario")
    senha: str = Field(..., min_length=6, max_length=18, description="A senha do usuario")