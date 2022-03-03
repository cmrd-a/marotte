import json
from dataclasses import dataclass, field, asdict
from datetime import datetime

from aiohttp import web, ClientSession, TCPConnector
from aiohttp.resolver import AsyncResolver

from settings import config


@dataclass
class Stub:
    path: str = field(default="/")
    id: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    body: dict = field(default_factory=dict)

    resp_status: int = field(default=200)
    resp_body: str = field(default="")
    resp_headers: dict = field(default_factory=dict)


stubs: [Stub] = list()

stubs.append(Stub(path="my", resp_body="my body"))


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    for stub in stubs:
        if name == stub.path:
            text = stub.resp_body
            return web.Response(text=text)

    resolver = AsyncResolver(nameservers=["8.8.8.8", "8.8.4.4"])
    conn = TCPConnector(resolver=resolver)
    async with ClientSession(connector=conn) as session:
        async with session.get(f"{config['http_real_address']}/{name}") as response:
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
    stub = Stub(**body)
    stubs.append(stub)
    return web.Response(body=json.dumps(asdict(stub)), content_type="application/json")

app = web.Application()
app['config'] = config
app.add_routes([
    web.get('/__stubs', get_stubs),
    web.post('/__stubs', create_stub),
    web.get('/', handle),
    web.get('/{name}', handle),
])

if __name__ == '__main__':
    web.run_app(app, port=8080)
