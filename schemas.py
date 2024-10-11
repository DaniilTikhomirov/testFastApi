from typing import Annotated

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: Annotated[
        str, Field(..., title="имя пользовотеля", min_length=2, max_length=50)
    ]
    surname: Annotated[
        str, Field(..., title="фамилия пользовотеля", min_length=2, max_length=50)
    ]
    age: Annotated[
        int, Field(..., title="возраст пользовотеля", ge=0)
    ]


class User(UserBase):
    id: Annotated[
        int, Field(..., title="id пользователя", ge=1)
    ]

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    news: Annotated[
        str, Field(..., title="новость поста", min_length=4)
    ]
    test: Annotated[
        str, Field(..., title="тест", min_length=4)
    ]

    author_id: Annotated[
        int, Field(..., title="id автора", ge=1)
    ]



class PostResponse(PostBase):
    id: Annotated[
        int, Field(..., title="id поста", ge=1)
    ]

    author: Annotated[
        User, Field(..., title="автор поста")
    ]

    class Config:
        orm_mode = True


class CreatePost(PostBase):
    pass


class UserCreate(UserBase):
    pass
