from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class LivroBase(BaseModel):
    titulo: str = Field(min_length=2, max_length=200)
    autor: str = Field(min_length=2, max_length=150)
    ano_publicacao: int | None = None
    disponivel: bool = True


class LivroCreate(LivroBase):
    pass


class LivroUpdate(BaseModel):
    """Todos os campos opcionais: só o que for enviado será atualizado."""

    titulo: str | None = Field(default=None, min_length=2, max_length=200)
    autor: str | None = Field(default=None, min_length=2, max_length=150)
    ano_publicacao: int | None = None
    disponivel: bool | None = None

    @field_validator("titulo", "autor", "disponivel")
    @classmethod
    def nao_aceitar_null(cls, v):
        # Campos obrigatórios/NOT NULL não podem ser anulados via PATCH
        if v is None:
            raise ValueError("Este campo não pode ser nulo")
        return v


class LivroResponse(LivroBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criado_em: datetime
