from core import utils
from core.logger import get_logger
from exceptions.core import APIException
from exceptions.error_messages import ErrorMessage
from fastapi import APIRouter, Request
import schemas

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


@router.get("/request-info", response_model=schemas.RequestInfoResponse)
def get_request_info(request: Request):
    ip_address = utils.get_request_info(request)
    host = utils.get_host_by_ip_address(ip_address)

    return schemas.RequestInfoResponse(ip_address=ip_address, host=host)
