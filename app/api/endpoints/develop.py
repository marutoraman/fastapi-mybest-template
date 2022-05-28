from core import utils
from core.logger import get_logger
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from fastapi import APIRouter, Request

logger = get_logger(__name__)

router = APIRouter()


@router.get("/error")
def exec_error() -> None:
    # time.sleep(100)
    logger.error("debug test")
    print(1 / 0)
    raise APIException(ErrorMessage.NOT_FOUND("デバックテストID"))


@router.get("/error2")
def exec_error2() -> None:
    # time.sleep(100)
    raise APIException(ErrorMessage.INTERNAL_SERVER_ERROR)


@router.get("/request-info")
def get_request_info(request: Request):
    return utils.get_request_info(request)
