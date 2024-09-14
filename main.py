import json
import os

import ssl
import aiohttp_cors
from aiohttp import web
from app.routes import setup_routes


async def setup_app():
    app = web.Application()

    setup_routes(app)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    for route in list(app.router.routes()):
        cors.add(route)

    return app

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        config = json.load(f)

    host_url = config['server']['host']
    port = config['server']['port']

    app = setup_app()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    cert_file = os.path.join(script_dir, 'cert.pem')
    key_file = os.path.join(script_dir, 'key.pem')

    if not os.path.isfile(cert_file) or not os.path.isfile(key_file):
        print(f"Error: cert.pem or key.pem file not found in {script_dir}")
        exit(1)

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)

    web.run_app(app, host=host_url, port=port, ssl_context=ssl_context)
