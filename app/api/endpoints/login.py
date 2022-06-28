import datetime

import crud
import schemas
from core import auth
from core.config import settings
from core.database import get_db
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> schemas.Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise APIException(ErrorMessage.FAILURE_LOGIN)
    # elif not crud.user.is_active(user):
    #     raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(user.id, expires_delta=access_token_expires)
    return schemas.Token(
        access_token=access_token,
        token_type="bearer",
    )
