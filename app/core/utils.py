import fastapi
import ulid
import socket
from fastapi import Request
from pkg_resources import require


def get_ulid() -> str:
    return ulid.new().str


def get_request_info(request: Request) -> str:
    return request.client.host


def get_host_by_ip_address(ip_address: str) -> str:
    return socket.gethostbyaddr(ip_address)[0]