from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
from app.dependencies.db import get_db
from app.dependencies.oauth2scheme import oauth2Scheme
from app.model import crud
# from app.utilities import dir_tool
from app.utilities.token_tools import get_user_name_by_token

likes_api = APIRouter(
    prefix="/likes",
    tags=['Likes'],
    dependencies=[Depends(get_db)],
    responses={
        404: {
            "Description": "Not Found"
        }
    }
)


@likes_api.get('/get/like_status')
async def get_like_status(post_uuid: str, db: Session = Depends(get_db), token: str = Depends(oauth2Scheme)):
    like_status = crud.get_like_status_from_database(post_uuid=post_uuid, db=db,
                                                     user_name=get_user_name_by_token(token=token))
    if like_status is None:
        return False
    else:
        return like_status


@likes_api.post("/send/like")
async def send_a_like_to_a_post(post_uuid: str, db: Session = Depends(get_db), token: str = Depends(oauth2Scheme)):
    if crud.write_like_status_in_database(db=db, post_uuid=post_uuid, user_name=get_user_name_by_token(token)):
        return {
            "status": "success"
        }
    elif crud.cancel_like_status_in_database(db=db, post_uuid=post_uuid, user_name=get_user_name_by_token(token)):
        return {
            "status": "success"
        }
    else:
        raise HTTPException(
            status_code=500,
            detail="Error"
        )
