from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
import os 
import time
from supabase import create_client, Client
import dotenv

dotenv.load_dotenv()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

app = FastAPI()

while True: 
    try:
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        supabase: Client = create_client(url, key)
        print("Supabase client created successfully")
        break
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        time.sleep(4)




@app.get("/")
async def read_root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    response = (
    supabase.table("Posts")
    .select("*")
    .limit(10)
    .execute()
)
    return {"posts": response.data}




@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    posts_dic = post.model_dump()
    response = (
        supabase.table("Posts")
        .insert(posts_dic)
        .execute()
    )
    return {"message": "Post created successfully", "post": response.data}


@app.get("/posts/{id}")
def get_post(id: int):
    response = (
        supabase.table("Posts")
        .select("*")
        .eq("id", id)
        .execute()
    )
    post = response.data
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return {"post": post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    response = (
        supabase.table("Posts")
        .delete()
        .eq("id", id)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    post_dict = post.model_dump()
    response = (
        supabase.table("Posts")
        .update(post_dict)
        .eq("id", id)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return Response(status_code=status.HTTP_205_RESET_CONTENT)