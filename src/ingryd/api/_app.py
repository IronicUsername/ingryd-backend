import json
import logging
from typing import Any

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import responder

from ._ingryd_extra import search, users

_LOGGER = logging.getLogger(__package__)


@responder
def app(environ: Any, start_response: Any) -> Any:
    request = Request(environ)

    url_map = Map([
        Rule('/users', methods=['GET', 'POST'], endpoint='users'),
        Rule('/search', methods=['GET'], endpoint='search'),
    ])

    endpoints = {
        'users': users,
        'search': search,
    }

    urls = url_map.bind_to_environ(environ)

    try:
        resp = urls.dispatch(lambda e, v: endpoints[e](request, **v))
    except HTTPException as e:
        resp = Response(json.dumps({'error': {'code': e.code, 'description': e.description}}).encode(),
                        content_type='application/json', status=e.code)

    _LOGGER.info(f'{request.remote_addr} @ '
                 f'"{request.method} {request.path} HTTP/1.1" {resp.status_code} '
                 f'{resp.calculate_content_length()} "{request.user_agent}"')

    return resp


def create_app():
    return app
