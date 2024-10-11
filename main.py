from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/")
async def home_page() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/contacts")
async def contacts() -> int:
    return 404


posts = [
    {"id": 1, "news": "news1", "test": "test1"},
    {"id": 2, "news": "news2", "test": "test2"},
    {"id": 3, "news": "news3", "test": "test3"},
    {"id": 4, "news": "news4", "test": "test4"},

]


def search(id: int) -> dict:
    for post in posts:
        if post["id"] == id:
            return post
    raise HTTPException(status_code=404, detail="post not found")


@app.get("/posts")
async def news() -> list[dict]:
    return posts


@app.get("/posts/{id}")
async def news(id: int) -> dict:
    return search(id)


@app.get("/search")
async def search_post(post_id: Optional[int] = None) -> dict:
    if post_id is None:
        return {"post": "not argument"}

    return search(post_id)
