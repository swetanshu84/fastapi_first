from fastapi import Body, Response, status,FastAPI , HTTPException, Depends, APIRouter
from .. import schema, database, model, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schema.Vote, db:Session = Depends(database.get_db), curr_user:int = Depends(oauth2.get_current_user)):
    
    post = db.query(model.Post).filter(model.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with ID : {vote.post_id} not exist!") # type: ignore
    
    vote_query = db.query(model.Vote).filter(
            model.Vote.post_id == vote.post_id, model.Vote.user_id == curr_user.id) # type: ignore
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User with ID : {curr_user.id} has already voted on post {vote.post_id}") # type: ignore
        new_vote = model.Vote(post_id=vote.post_id, user_id=curr_user.id) # type: ignore
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message" : "Vote added successfully"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=" Vote not exist !") # type: ignore
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : "Vote deleted successfully"}