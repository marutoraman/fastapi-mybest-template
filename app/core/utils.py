import fastapi
import ulid
from fastapi import Request
from pkg_resources import require


def get_ulid() -> str:
    return ulid.new().str


def get_request_info(request: Request):
    return request.client.host
