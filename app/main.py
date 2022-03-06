import json
import logging
from dataclasses import dataclass, field, asdict
from datetime import datetime

from aiohttp import web, ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver

from settings import config


@dataclass
class Stub:
    method: str = field(default="GET")
    path: str = field(default="/")
    id: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    body: dict = field(default_factory=dict)

    resp_status: int = field(default=200)
    resp_body: str = field(default="")
    resp_headers: dict = field(default_factory=dict)


stubs: [Stub] = [
    Stub(path="/my", resp_body="my body"),
    Stub(method="POST", path="/my", body={"id": 21}, resp_body="my body 21"),
    Stub(method="POST", path="/my", body={"id": 42}, resp_body="my body 42"),
]


async def handle(request):
    path = request.raw_path
    for stub in stubs:
        if request.method == stub.method and path == stub.path:
            if request.method == "POST" and request.has_body:
                req_body = await request.json()
                if req_body != stub.body:
                    continue
            text = stub.resp_body
            return web.Response(text=text)

    resolver = AsyncResolver(nameservers=["8.8.8.8"])
    conn = TCPConnector(resolver=resolver)  # windows slow dns fix
    async with ClientSession(connector=conn) as session:
        async with session.get(f"{config['http_real_address']}{path}") as response:
            print("Status:", response.status)
            html = await response.text()
            return web.Response(text=html[:20])


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


app = web.Application()
logging.basicConfig(level=logging.DEBUG)
app['config'] = config
app.add_routes([
    web.get('/__stubs', get_stubs),
    web.post('/__stubs', create_stub),
    web.get('/{path_var:.*}', handle),
    web.post('/{path_var:.*}', handle),
])

if __name__ == '__main__':
    web.run_app(app, port=8080)
