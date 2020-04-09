import logging
import logging.config
import os


def init():
    working_dir = os.path.dirname(os.path.abspath(__file__))

    if os.environ.get('LOG_CONSOLE', '0') == '1':
        conf_file = os.path.join(working_dir, 'logging-dev.conf')
    else:
        conf_file = os.path.join(working_dir, 'logging.conf')

    with open(str(conf_file), 'r', encoding='utf-8') as f:
        logging.config.fileConfig(f, disable_existing_loggers=False)

    logging.getLogger().setLevel(os.environ.get('LOG_LEVEL', 'DEBUG'))
