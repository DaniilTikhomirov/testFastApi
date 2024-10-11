from typing import Optional, List, Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int


class Post(BaseModel):
    id: int
    news: str
    test: str
    author: User

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

users = [
    {"name": "Jhon", "surname": "Smith", "age": 25},
    {"name": "Alex", "surname": "Kyrsov", "age": 25},
    {"name": "Fedor", "surname": "Tyson", "age": 25},
]


posts = [
    {"id": 1, "news": "news1", "test": "test1", "author": users[0]},
    {"id": 2, "news": "news2", "test": "test2", "author": users[1]},
    {"id": 3, "news": "news3", "test": "test3", "author": users[2]},
    {"id": 4, "news": "news4", "test": "test4", "author": users[0]},

]


@app.get("/")
async def home_page() -> dict[str, str]:
    return {"message": "Hello World"}


@app.get("/contacts")
async def contacts() -> int:
    return 404


def search(id: int) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post.from_dict(post)
    raise HTTPException(status_code=404, detail="post not found")


@app.get("/posts")
async def news() -> list[Post]:
    return [Post(**d) for d in posts]


@app.get("/posts/{id}")
async def news(id: int) -> Post:
    return search(id)


@app.get("/search")
async def search_post(post_id: Optional[int] = None) -> Dict[str, Optional[Post]]:
    if post_id is None:
        return {"post": None}

    return {"post": search(post_id)}
