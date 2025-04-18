import logging

import uvicorn

from api import create_app
from notifiers.log_notifier import LogNotify


def main():
    notifiers = [LogNotify()]
    app = create_app(notifiers)
    uvicorn.run(app, host='0.0.0.0', port=5001, log_level='debug')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    main()