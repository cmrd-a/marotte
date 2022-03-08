import json
from dataclasses import asdict

from aiohttp import web, ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver

from app.models import stubs, Stub
from settings import config


async def handle_get(request):
    path = request.raw_path
    for stub in stubs:
        if stub.method == "GET" and path == stub.path:
            return web.Response(text=stub.resp_body)

    resolver = AsyncResolver(nameservers=["8.8.8.8"])
    conn = TCPConnector(resolver=resolver)  # windows slow dns fix
    async with ClientSession(connector=conn) as session:
        async with session.get(f"{config['http_target_address']}{path}") as response:
            resp_text = await response.text()
            return web.Response(text=resp_text)


async def handle_post(request):
    path = request.raw_path
    req_body = await request.json() if request.has_body else None
    for stub in stubs:
        if stub.method == "POST" and path == stub.path:
            if req_body != stub.body:
                continue
            text = stub.resp_body
            return web.Response(text=text)

    resolver = AsyncResolver(nameservers=["8.8.8.8"])
    conn = TCPConnector(resolver=resolver)  # windows slow dns fix
    async with ClientSession(connector=conn) as session:
        async with session.post(f"{config['http_target_address']}{path}", json=req_body) as response:
            resp_text = await response.text()
            return web.Response(text=resp_text)


async def get_stubs(request):
    # todo: limit, offset
    resp_dict = {
        "quantity": len(stubs),
        "stubs": [asdict(stub) for stub in stubs]
    }
    return web.Response(body=json.dumps(resp_dict), content_type="application/json")


async def create_stub(request):
    body = await request.json()
    stub = Stub(**body)  # todo: list of subs
    stubs.append(stub)
    return web.Response(body=json.dumps(asdict(stub)), content_type="application/json")


def setup_routes(app):
    app.router.add_get('/__stubs', get_stubs)
    app.router.add_post('/__stubs', create_stub)

    app.router.add_get('/{path_var:.*}', handle_get)
    app.router.add_post('/{path_var:.*}', handle_post)
