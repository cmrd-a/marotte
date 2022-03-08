import logging

from aiohttp import web

from app.routes import setup_routes
from app.settings import config


def main():
    app = web.Application()
    setup_routes(app)
    logging.basicConfig(level=logging.DEBUG)
    web.run_app(app, host=config["app_host"], port=config["app_port"])


if __name__ == '__main__':
    main()
