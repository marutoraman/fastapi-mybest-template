import models
import schemas
from sqlalchemy.orm import Session

from .base import CRUDBase


class CRUDHashtag(CRUDBase[models.Job, schemas.JobCreate, schemas.JobUpdate, schemas.JobsPagedResponse]):
    SELECT_QUERY = [models.Job.id, models.Job.title, models.Job.updated_at]

    def get(self, db: Session, id: str, include_deleted: bool = False):
        return super().get(db, id=id, include_deleted=include_deleted, select_query=self.SELECT_QUERY)


job = CRUDHashtag(models.Job, schemas.JobsPagedResponse(data=[], meta=None))
