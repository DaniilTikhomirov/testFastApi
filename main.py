from typing import Optional, List, Dict, Annotated

from fastapi import FastAPI, HTTPException, Path
from fastapi.params import Query, Body, Depends
from sqlalchemy.orm import Session

from models import User, Post, Base
from database import engine, session_local
from schemas import UserCreate,User as dbUser, CreatePost, PostResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=dbUser)
def create_user(user: Annotated[UserCreate, Body(..., example={
    "name": "Jhon",
    "surname": "Smith",
    "age": 25
})], db: Session = Depends(get_db)) -> dbUser:
    db_user = User(name=user.name, surname=user.surname, age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@app.post("/post/", response_model=PostResponse)
def create_user(post: Annotated[CreatePost, Body(..., example={
    "news" : "news",
    "test" : "test",
    "author_id" : 1
})], db: Session = Depends(get_db)) -> PostResponse:
    db_user = db.query(User).filter(User.id == post.author_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_post = Post(news=post.news, test=post.test, author_id=post.author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

@app.get("/posts/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)) -> List[PostResponse]:
    db_posts = db.query(Post).all()
    return db_posts


# @app.get("/")
# async def home_page() -> dict[str, str]:
#     return {"message": "Hello World"}
#
#
# def search(id: int) -> Post:
#     for post in posts:
#         if post["id"] == id:
#             return Post(**post)
#     raise HTTPException(status_code=404, detail="post not found")
#
#
# @app.get("/posts")
# async def all_post() -> list[Post]:
#     return [Post(**d) for d in posts]
#
#
# @app.post("/posts/add")
# async def add_post(post: CreatePost) -> Post:
#     author = next((user for user in users if user["id"] == post.author_id), None)
#     if author is None:
#         raise HTTPException(status_code=404, detail="author not found")
#
#     new_id = max(p["id"] for p in posts) + 1
#     new_post = {"id": new_id, "news": post.news, "test": post.test, "author": author}
#
#     posts.append(new_post)
#
#     return Post(**new_post)
#
#
# @app.post("/user/add")
# async def add_user(user: Annotated[UserCreate,
# Body(..., example={
#     "name": "Jhon",
#     "surname": "Smith",
#     "age": 25
# })]) -> User:
#     new_id = max(p["id"] for p in posts) + 1
#     new_user = {"id": new_id, "name": user.name, "surname": user.surname, "age": user.age}
#     users.append(new_user)
#     return User(**new_user)
#
#
# @app.get("/posts/{id}")
# async def news(id: Annotated[int, Path(..., title='id поста', ge=1, lt=100)]) -> Post:
#     return search(id)
#
#
# @app.get("/search")
# async def search_post(post_id: Annotated[Optional[int],
# Query(title='id для поиска поста', ge=1, lt=100)] = None) -> Dict[str, Optional[Post]]:
#     if post_id is None:
#         return {"post": None}
#
#     return {"post": search(post_id)}
