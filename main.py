from typing import Optional, List, Dict, Annotated

from fastapi import FastAPI, HTTPException, Path
from fastapi.params import Query, Body
from pydantic import BaseModel, Field

app = FastAPI()



class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class Post(BaseModel):
    id: int
    news: str
    test: str
    author: User

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class CreatePost(BaseModel):
    news: str
    test: str
    author_id: int

class UserCreate(BaseModel):
    name: Annotated[
        str, Field(..., title="имя пользовотеля", min_length=2, max_length=50)
    ]
    surname: Annotated[
        str, Field(..., title="фамилия пользовотеля", min_length=2, max_length=50)
    ]
    age: Annotated[
        int, Field(..., title="возраст пользовотеля", min_length=2, max_length=50)
    ]


users = [
    {"id": 1, "name": "Jhon", "surname": "Smith", "age": 25},
    {"id": 2, "name": "Alex", "surname": "Kyrsov", "age": 25},
    {"id": 3, "name": "Fedor", "surname": "Tyson", "age": 25},
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


def search(id: int) -> Post:
    for post in posts:
        if post["id"] == id:
            return Post.from_dict(post)
    raise HTTPException(status_code=404, detail="post not found")


@app.get("/posts")
async def all_post() -> list[Post]:
    return [Post.from_dict(d) for d in posts]


@app.post("/posts/add")
async def add_post(post: CreatePost) -> Post:
    author = next((user for user in users if user["id"] == post.author_id), None)
    if author is None:
        raise HTTPException(status_code=404, detail="author not found")

    new_id = max(p["id"] for p in posts) + 1
    new_post = {"id": new_id, "news": post.news, "test": post.test, "author": author}

    posts.append(new_post)

    return Post.from_dict(new_post)


@app.post("/user/add")
async def add_user(user: Annotated[UserCreate,
Body(..., example={
    "name": "Jhon",
    "surname": "Smith",
    "age": 25
})]) -> User:
    new_id = max(p["id"] for p in posts) + 1
    new_user = {"id": new_id, "name": user.name, "surname": user.surname, "age": user.age}
    users.append(new_user)
    return User.from_dict(new_user)



@app.get("/posts/{id}")
async def news(id: Annotated[int, Path(..., title='id поста', ge=1, lt=100)]) -> Post:
    return search(id)


@app.get("/search")
async def search_post(post_id: Annotated[Optional[int],
Query(title='id для поиска поста', ge=1, lt=100)] = None) -> Dict[str, Optional[Post]]:
    if post_id is None:
        return {"post": None}

    return {"post": search(post_id)}
