from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

class Post(BaseModel):
    title: str
    content: str
    id: int | None = None
    published: bool = True
    rating: int | None = None

app = FastAPI()


# Save data in memory
posts = [
    {"title": "My first post", "content": "This is my first post", "id": 1},
    {"title": "My second post", "content": "This is my second post", "id": 2},
    {"title": "My third post", "content": "This is my third post", "id": 3}
         
]


@app.get("/")
async def read_root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"posts": posts}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    posts_dic = post.model_dump()
    posts_dic["id"] = randrange(0, 1000000)
    posts.append(posts_dic)
    return {"message": "Post created successfully", "post": posts_dic}


@app.get("/posts/{id}")
def get_post(id: int):
    post = next((post for post in posts if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    post = next((post for post in posts if post["id"] == id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts.pop(posts.index(post))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_dict = post.model_dump()
    existing_post = next((post for post in posts if post["id"] == id), None)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    posts.pop(posts.index(existing_post))
    post_dict["id"] = randrange(0, 1000000)
    posts.append(post_dict)
    return Response(status_code=status.HTTP_205_RESET_CONTENT)