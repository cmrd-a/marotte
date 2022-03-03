import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    name: str | None = None


app = FastAPI()

items_list = [
    Item(item_id=0, name="item0"),
    Item(item_id=1, name="item1"),
]


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


@app.post("/shitty_post/")
async def create_item(item: Item):
    return items_list[item.item_id]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
