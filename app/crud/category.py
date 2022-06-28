import models
import schemas

from .base import CRUDBase, Session


class CRUDCategory(
    CRUDBase[
        models.Category,
        schemas.CategoryCreate,
        schemas.CategoryUpdate,
        schemas.CategoriesPagedResponse,
    ]
):
    def updat_parent_category(self, db: Session, db_obj: models.Category, parent_category_id: str) -> models.Category:
        db_obj.parent_category_id = parent_category_id
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        return db_obj


category = CRUDCategory(models.Category, schemas.CategoriesPagedResponse(data=[], meta=None))
