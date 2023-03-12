from fastapi import Body, Response, status,FastAPI , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from .. import database , schema , model, utils, oauth2
router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schema.Token)
async def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)):
    
    #OAuth2PasswordRequestForm return only username and password ; 


    user = db.query(model.User).filter(model.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password!")
    
    if not utils.verify(user_credentials.password, user.password):  # type: ignore
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid username or password!")
    
    #create token for authentication
    # return token
    create_token = oauth2.create_access_token(data={"user_id":user.id})
    return  {"access_token": create_token, "token_type":"bearer"}