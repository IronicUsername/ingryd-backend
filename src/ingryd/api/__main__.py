import logging
from os import environ
import signal

from ingryd.api._app import create_app
from ingryd.database import create_db
from ingryd.utility import sigterm_handler

_LOGGER = logging.getLogger(__package__)
HOST = '0.0.0.0'
PORT = 80
RELOADER = int(environ.get('RELOADER', '0')) == 1
RUN_WITH_CHEROOT = int(environ.get('RUN_WITH_CHEROOT', '0')) == 1

signal.signal(signal.SIGTERM, sigterm_handler)

setup_db_version = create_db()
_LOGGER.info(f'Starting `ingryd` API on {HOST}:{PORT}.')

app = create_app()

if not RUN_WITH_CHEROOT:
    from werkzeug.serving import run_simple

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    run_simple(HOST, PORT, app, use_reloader=RELOADER)
else:
    from cheroot import wsgi

    server = wsgi.Server((HOST, PORT), app)

    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
