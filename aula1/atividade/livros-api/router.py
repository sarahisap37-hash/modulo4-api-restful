from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Livro
from schemas import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def _get_or_404(livro_id: int, db: Session) -> Livro:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Livro não encontrado")
    return livro


@router.get("", response_model=list[LivroResponse])
def listar_livros(db: Session = Depends(get_db)):
    """Lista todos os livros disponíveis."""
    stmt = select(Livro).where(Livro.disponivel.is_(True)).order_by(Livro.id)
    return db.scalars(stmt).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    """Busca um livro pelo ID (404 se não existir)."""
    return _get_or_404(livro_id, db)


@router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    """Cria um novo livro."""
    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.patch("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_db)):
    """Atualiza apenas os campos enviados."""
    livro = _get_or_404(livro_id, db)
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    """Soft delete: marca disponivel=False, sem apagar o registro."""
    livro = _get_or_404(livro_id, db)
    livro.disponivel = False
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
