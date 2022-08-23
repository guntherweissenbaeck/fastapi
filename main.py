from random import randrange
from typing import Optional
from unicodedata import name

from fastapi import FastAPI
from pydantic import BaseModel

import uvicorn

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [
    {"title": "title post 1", "content": "content post 1", "id": 1},
    {"title": "title post 2", "content": "content post 2", "id": 2}

]


def find_post(id):
    # [{'title': 'title post 1', 'content': 'content post 1', 'id': 1}, {'title': 'title post 2', 'content': 'content post 2', 'id': 2}]
    for post in my_posts:
        if post["id"] == id:
            return post


def del_post(id):
    c = 0
    for post in my_posts:
        if post["id"] == id:
            del my_posts[c]
            return my_posts
        else:
            c += 1


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.get('/posts/{id}')
def get_posts(id: int):
    post = find_post(id)
    return {'data': post}


@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(10, 999)
    my_posts.append(post_dict)
    return {'data': post_dict}


@app.patch('/posts/{id}')
def update_post(id: int, post: Post):
    pass


@app.delete('/posts/{id}')
def delete_post(id: int):
    del_post(id)
    return {'data': f"post with id {id} was deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
