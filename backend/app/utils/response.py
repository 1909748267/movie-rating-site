from typing import Any, Optional


def success_response(data: Any = None, message: str = "操作成功") -> dict:
    response = {
        "code": "SUCCESS",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response


def error_response(code: str, message: str) -> dict:
    return {
        "code": code,
        "message": message
    }
