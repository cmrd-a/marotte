import pathlib

import uvicorn
import yaml
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    name: str | None = None


app = FastAPI()

items_list = []
for i in range(2):
    items_list.append(Item(item_id=i, name=f"item-{i}"))


@app.get("/items")
async def get_list():
    return {"data": items_list}


@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"data": items_list[item_id]}


@app.post("/items/")
async def create_item(item: Item):
    items_list.append(item)
    return item


@app.post("/post-but-get/")
async def post_but_get(item: Item):
    return items_list[item.item_id]


if __name__ == "__main__":
    BASE_DIR = pathlib.Path(__file__).parent
    config_path = BASE_DIR / 'config.yaml'
    with open(config_path) as f:
        conf = yaml.safe_load(f)

    uvicorn.run(app, host="0.0.0.0", port=conf['http_target_port'])
