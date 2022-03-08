import json
from dataclasses import asdict

from aiohttp import web, ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver

from app.models import stubs, Stub
from settings import config


async def make_stub_resp(stub: Stub) -> web.Response:
    stub.resp_count += 1
    return web.Response(body=json.dumps(stub.resp_body), status=stub.resp_status, headers=stub.resp_headers)


async def handle(request):
    method = request.method
    path = request.raw_path
    req_body = await request.json() if request.has_body else None
    for stub in stubs:
        if path == stub.path:
            if stub.method == "GET":
                return await make_stub_resp(stub)
            else:
                if req_body != stub.body:
                    continue
                return await make_stub_resp(stub)

    resolver = AsyncResolver(nameservers=["8.8.8.8"])
    conn = TCPConnector(resolver=resolver)  # Windows slow dns fix
    async with ClientSession(connector=conn) as session:
        async with session.request(method, f"{config['http_target_address']}{path}", json=req_body,
                                   headers=request.headers) as resp:
            resp_body = await resp.read()
            return web.Response(body=resp_body, status=resp.status, headers=resp.headers)


async def get_stubs(request):
    # todo: limit, offset
    resp_dict = {
        "quantity": len(stubs),
        "stubs": [asdict(stub) for stub in stubs]
    }
    return web.json_response(data=resp_dict)


async def create_stub(request):
    body = await request.json()
    stub = Stub(**body)  # todo: list of subs, upsert
    stubs.append(stub)
    return web.json_response(data=asdict(stub))


def setup_routes(app):
    app.router.add_get('/__stubs', get_stubs)
    app.router.add_post('/__stubs', create_stub)

    app.router.add_get('/{path_var:.*}', handle)
    app.router.add_post('/{path_var:.*}', handle)
