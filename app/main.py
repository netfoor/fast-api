from fastapi import FastAPI
from .database import create_db_and_tables
from contextlib import asynccontextmanager
from .routes import post, user, auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        print("🛠️ Database and tables created successfully")
    except Exception as e:
        print(f"Error creating database and tables: {e}")
    yield

    print("🛠️ Application shutting down...")


app = FastAPI(lifespan=lifespan)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)