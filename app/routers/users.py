from fastapi import Body, Response, status,FastAPI , HTTPException, Depends, APIRouter
from .. import model, schema, utils
from sqlalchemy.orm import Session
from ..database import  get_db

router = APIRouter(
    prefix="/users",
    tags=["Users-APIs"]
); 

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut) 
def create_user(params:schema.UserCreate, db:Session = Depends(get_db)):
    #hash the password for the user
    hashed_pass = utils.hash(params.password)
    params.password = hashed_pass
    new_user = model.User(**params.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return  new_user
 
@router.get("/{id}",response_model=schema.UserOut ,status_code=status.HTTP_201_CREATED)
def get_users(id:int, db:Session = Depends(get_db)):
    users = db.query(model.User).filter(model.User.id == id).first()

    if not users :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {id} was not found!")
    return   users