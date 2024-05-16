import logging
import base64
from django.utils import timezone


def get_time_string():
    return timezone.make_naive(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")


def get_request_headers(request):
    headers = {}
    for key, value in request.META.items():
        if key.startswith("HTTP_"):
            headers[key] = value
    return headers


def get_request_log_text(data):
    if isinstance(data, str):
        return data
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return data.decode("gb18030")
        except UnicodeDecodeError:
            return "application/data;base64:" + "".join(
                base64.encodebytes(data).decode().splitlines()
            )
