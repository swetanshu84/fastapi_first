from fastapi import Body, Response, status,FastAPI , HTTPException, Depends, APIRouter
from .. import model, schema, oauth2
from typing import  List
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from ..database import  get_db 

from ..config import settings

import psycopg2
from psycopg2.extras import RealDictCursor
import time

# f'postgresql://{settings.DATABASE_USER}:[{settings.DATABASE_PASSWORD}]:@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'
while True:
    try:
        conn = psycopg2.connect(host=f'{settings.DATABASE_HOST}',database=f'{settings.DATABASE_NAME}',user=f'{settings.DATABASE_USER}',password=f'{settings.DATABASE_PASSWORD}',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection is success")
        break
    except Exception as error:
        print("Database connection failed !")
        print("Error : ", error)
        time.sleep(2)

# cursor = get_db()
router = APIRouter(
    prefix="/posts",
    tags=["Posts-APIs"]
); 


# @router.get("/" ,response_model=List[schema.PostResponse])
@router.get("/" )
def get_posts(db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user),
                    limit:int=10, skip:int = 0,search:Optional[str]="") :
    
    # posts = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
    #    model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).limit(limit).offset(skip)
    # its not working with with sqlalchemy
    
    cursor.query(""" SELECT posts.id AS posts_id, posts.owner_id AS posts_owner_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at, count(votes.post_id) AS votes 
FROM posts LEFT OUTER JOIN votes ON votes.post_id = posts.id GROUP BY posts.id """)
    posts = cursor.fetchall()
    print(posts)
    return posts
    # return   posts # type: ignore
 


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.PostResponse) # Set default status code
def create_post(params:schema.CreatePostDt, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    # new_post = model.Post(title=params.title, content=params.content, published=params.published)
    new_post = model.Post(owner_id=curr_user.id, **params.dict()) # type: ignore
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post
 

# @router.get('/{id}',response_model=schema.PostOut)
@router.get('/{id}',response_model=schema.PostResponse)
def get_post(id:str, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
   
    post = db.query(model.Post).filter(model.Post.id == id).first()
    # post = db.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
    #    model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).filter(model.Post.id == id).first()
    if not post :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found !")
        
    return  post 
 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    
    if post.owner_id != curr_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to performe required action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.PostResponse)
def update_post(id:int, updated_post:schema.PostDt, db:Session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user)):
    post_qry = db.query(model.Post).filter(model.Post.id == id)
    post = post_qry.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" Post with : {id} does not exist .")
    post_qry.update(updated_post.dict(), synchronize_session=False) # type: ignore
    db.commit()
    # return {"message : ": "Post updated"}
    return   post_qry.first()
