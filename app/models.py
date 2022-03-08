from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Stub:
    method: str = field(default="GET")
    path: str = field(default="/")
    body: dict = field(default=None)

    resp_status: int = field(default=200)
    resp_body: dict = field(default_factory=dict)
    resp_headers: dict = field(default_factory=dict)

    id: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    resp_count: int = field(default=0)


stubs: [Stub] = [
    Stub(path="/my", resp_body={"data": "some data"}, resp_headers={"content-type": "applications/json"}),
    Stub(method="POST", path="/my", body={"id": 21}, resp_body={"data": "data 21"}),
    Stub(method="POST", path="/my", body={"id": 42}, resp_body={"data": "data 42"}),
]
