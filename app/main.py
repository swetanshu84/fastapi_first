from fastapi import FastAPI 
from .config import Settings
from . import model
from .database import engine
# from fastapi.params import Body
from .routers import posts, users ,auth, vote
from fastapi.middleware.cors import CORSMiddleware


# model.Base.metadata.create_all(bind=engine)
        
app = FastAPI()
# origins = ["https://www.google.com/"] # for list of origins
origins = ["*"] # all urls can access our api origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)
 
 
@app.get("/")
async def root():
    return {"message": "Welcome to fastapi v1 "}
 