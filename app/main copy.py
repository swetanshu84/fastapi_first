from typing import Optional
from fastapi import Body, Response, status,FastAPI , HTTPException
from pydantic import BaseModel
# from fastapi.params import Body
from random import randrange # generate random number
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

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
    params_dict = params.dict()
    params_dict['id'] = randrange(0,100000000)
    my_posts.append(params_dict)
    return {"Message"  : my_posts}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"Latest Post : ": post}


@app.get('/posts/{id}')
def get_post(id:int):
    post = find_post(id) ; 
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found !")
        
    return { " Post Details : ":post }

# @app.get('/posts/{id}')
# def get_post(id:int, respo:Response):
#     post = find_post(id) ; 
#     if not post :
#         respo.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": f"Post with id {id} was not found !"}
#     return { " Post Details : ":post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    #deteling post
    # Find the index of post that has required ID
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    my_posts.pop(index)  # type: ignore
    # return {"message" : " Post was successfully deleted !"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:PostDt):
    print(post)
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    post_dict = post.dict() 
    post_dict['id'] = id

    my_posts[index] = post_dict
    # return {"message : ": "Post updated"}
    return { "Date : ": my_posts}

