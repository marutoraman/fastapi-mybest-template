from typing import Optional

import crud
import models
import schemas
from core.database import get_db
from core.logger import get_logger
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from fastapi import APIRouter, Depends
from schemas.core import PagingQueryIn
from sqlalchemy.orm import Session

logger = get_logger(__name__)

router = APIRouter()


@router.get("/{id}", response_model=schemas.CategoryResponse)
def get_job(id: str, db: Session = Depends(get_db)) -> models.Category:
    category = crud.category.get(db, id=id)
    if not category:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return category


@router.get("", response_model=schemas.CategoriesPagedResponse)
def get_categories(
    q: Optional[str] = None,
    paging: PagingQueryIn = Depends(),
    db: Session = Depends(get_db),
) -> schemas.CategoriesPagedResponse:
    if q:
        query = db.query(models.Category).filter(models.Category.name.like(f"%{q}%"))
    else:
        query = db.query(models.Category)
    print(query)
    return crud.category.get_paged_list(db, paging=paging, filtered_query=query)


@router.post("", response_model=schemas.CategoryResponse)
def create_category(data_in: schemas.CategoryCreate, db: Session = Depends(get_db)) -> models.Category:
    try:
        return crud.category.create(db, data_in)
    except Exception:
        import traceback

        logger.error(str(traceback.format_exc()))


@router.put("/{id}", response_model=schemas.CategoryResponse)
def update(
    id: str,
    data_in: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
) -> models.Category:
    category = db.query(models.Category).filter_by(id=id).first()
    if not category:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    if data_in.parent_category_id:
        if not db.query(models.Category).filter_by(id=data_in.parent_category_id).first():
            raise APIException(ErrorMessage.NOT_FOUND("parent_category_id"))
    return crud.category.update(db, db_obj=category, obj_in=data_in)


@router.delete("/{id}", response_model=schemas.CategoryResponse)
def delete(
    id: str,
    db: Session = Depends(get_db),
) -> models.Category:
    category = db.query(models.Category).filter_by(id=id).first()
    if not category:
        raise APIException(ErrorMessage.ID_NOT_FOUND)
    return crud.category.delete(db, db_obj=category)
