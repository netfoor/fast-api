from fastapi import FastAPI
from contextlib import asynccontextmanager
from .routes import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # try:
    #     create_db_and_tables()
    #     print("🛠️ Database and tables created successfully")
    # except Exception as e:
    #     print(f"Error creating database and tables: {e}")
    print("🚀 Application starting up...")
    yield
    print("🛠️ Application shutting down...")


app = FastAPI(lifespan=lifespan)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World from Render using Trigger for docker image!"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)