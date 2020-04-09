import json
from typing import Any

from werkzeug.wrappers import Request, Response

from .users import request_users


def search(requ: Request, **kwargs: Any) -> Response:
    res = {'msg': 'hi'}
    return Response(json.dumps(res, indent=4).encode(), content_type='application/json')


def users(requ: Request, **kwargs: Any) -> Response:
    res = request_users()
    return Response(json.dumps(res, indent=4).encode(), content_type='application/json')
