import json
import logging
from typing import Any

from werkzeug.wrappers import Request, Response

from ingryd.database import query
from .users import request_users

_LOGGER = logging.getLogger(__package__)


def healty(req: Request) -> Response:
    """Check service health.

    Parameters
    ----------
    req: Request
        Object with all data associated with HTTP Request.

    Returns
    -------
    response: Response
        Result of 'GET /healty' call.
    """
    try:
        with query('SELECT 1 from production_db_version;'):
            pass
    except Exception as e:
        _LOGGER.exception("Ingryd\'s connection to the database faild. "
                          f'Error: {e}')
        return Response(b'', content_type='text/plain', status=503)

    return Response(b'', content_type='text/plain', status=204)


def search(requ: Request, **kwargs: Any) -> Response:
    res = {'msg': 'hi'}
    return Response(json.dumps(res, indent=4).encode(), content_type='application/json')


def users(requ: Request, **kwargs: Any) -> Response:
    res = request_users()
    return Response(json.dumps(res, indent=4).encode(), content_type='application/json')
