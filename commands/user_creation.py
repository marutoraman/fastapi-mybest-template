import __set_base_path__
import fire

import crud
import models
import schemas
from core.database import get_db


def create_user(email: str, full_name: str, password: str) -> models.User:
    db = next(get_db())
    user = crud.user.create(db, obj_in=schemas.UserCreate(full_name=full_name, email=email, password=password))
    print(user.to_dict())

    return user


if __name__ == "__main__":
    fire.Fire(create_user)
