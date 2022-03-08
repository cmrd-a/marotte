from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Stub:
    method: str = field(default="GET")
    path: str = field(default="/")
    id: float = field(default_factory=lambda: datetime.utcnow().timestamp())
    body: dict = field(default=None)

    resp_status: int = field(default=200)
    resp_body: str = field(default="")
    resp_headers: dict = field(default_factory=dict)


stubs: [Stub] = [
    Stub(path="/my", resp_body="my body"),
    Stub(method="POST", path="/my", body={"id": 21}, resp_body="my body 21"),
    Stub(method="POST", path="/my", body={"id": 42}, resp_body="my body 42"),
]
