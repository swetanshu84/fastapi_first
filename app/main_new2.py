from typing import Optional
from fastapi import Body, Response, status,FastAPI , HTTPException
from pydantic import BaseModel
# from fastapi.params import Body
from random import randrange # generate random number
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from . import model
from .database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Validate post value and keys
class PostDt(BaseModel):
    title:str
    content:str
    published:bool = True 
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi_db',user='swetanshudubey',password='Sekhar@123',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is success")
        break
    except Exception as error:
        print("Database connection failed !")
        print("Error : ", error)
        time.sleep(2)


#save data in memory globly
my_posts = [
    {"id":1,"title":"title of post 1", "content":"content of post 1"},
    {"id":2,"title":"Favorite foods", "content":"I like pizza"}
    ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id :
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i       

@app.get("/")
async def root():
    return {"message": "Welcome to fastapi v1 "}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    allPosts = cursor.fetchall()
    return {"data":  allPosts}


@app.post("/posts", status_code=status.HTTP_201_CREATED) # Set default status code
def create_post(params:PostDt):
    # print(params.dict()) # Convert pydantic to directory ; 
    cursor.execute(""" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(params.title,params.content,params.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Message"  : new_post}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"Latest Post : ": post}


@app.get('/posts/{id}')
def get_post(id:str):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone() 
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found !")
        
    return { " Post Details : ":post }
 
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """,(str(id),))
    #deteling post
    # Find the index of post that has required ID
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:PostDt):
    cursor.execute(""" UPDATE posts SET  title = %s, content = %s , published= %s  where id = %s returning * """, 
    (post.title, post.content, post.published, str(id)))
    conn.commit()
    update_post = cursor.fetchone()
    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    
    # return {"message : ": "Post updated"}
    return { "Updated Post : ": update_post}

