from typing import Dict, Generator

import pytest
from core.config import settings
from core.database import get_db
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .utils.test_crud import init_tables
# from tests.utils.test_crud import init_tables
from .utils.user import authentication_token_from_email

# from tests.utils.user import authentication_token_from_email

# from tests.utils.utils import get_superuser_token_headers


# engine = create_engine(f"{settings.TEST_DATABASE_URI}?charset=utf8mb4")
# clear_and_set_test_data(engine)

# test_session = scoped_session(
#     sessionmaker(autocommit=False, autoflush=False, bind=engine)
# )
# テスト専用のDBを使用する
engine = create_engine(f"{settings.TEST_DATABASE_URI}?charset=utf8mb4")


def get_test_db() -> Generator:
    # engine = create_engine(f"{settings.TEST_DATABASE_URI}?charset=utf8mb4")

    # テストデータをセット
    # clear_and_set_test_data(engine)

    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = test_session()
    try:
        yield db
    finally:
        # rollbackすることで、clearなDBを維持する
        db.rollback()
        db.close()


@pytest.fixture()
def clear_db():
    init_tables(engine)


@pytest.fixture
def db() -> Generator:
    # test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # settings of test database
    # clear_and_set_test_data(engine)
    init_tables(engine)
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = test_session()

    try:
        yield db
    finally:
        # rollbackすることで、clearなDBを維持する
        db.rollback()
        db.close()


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        init_tables(engine)
        app.dependency_overrides[get_db] = get_test_db
        # try:
        yield c
        # finally:
        #     app.dependency_overrides[get_db] = get_db


# @pytest.fixture(scope="module")
# def admin_user_token_headers(client: TestClient) -> Dict[str, str]:
#     return get_superuser_token_headers(client)


@pytest.fixture
def auth_headers(client: TestClient, db: Session) -> Dict[str, str]:
    return authentication_token_from_email(
        client=client, email=settings.TEST_USER_EMAIL, db=db
    )


# def TestSession():
#     """
#     テスト用のＤＢと接続し、テストデータをセットするための処理
#     テスト関数実行毎に呼ばれるfixture
#     """
#     # settings of test database
#     engine = create_engine(f"{settings.TEST_DATABASE_URI}?charset=utf8mb4")

#     # tableを初期化
#     init_tables(engine)

#     test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     # Run the tests
#     yield test_session
