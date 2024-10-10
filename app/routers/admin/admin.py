from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from pathlib import Path
from fastapi.responses import JSONResponse

from app.dependencies.oauth2scheme import oauth2Scheme
from app.dependencies.db import get_db
from app.utilities import admin_tool, dir_tool
from app.model import schemas, crud
from pyecharts.charts import Line, Funnel
from pyecharts import options as opts
from fastapi.encoders import jsonable_encoder
from app import config

admin_auth_router = APIRouter(
    prefix="/admin",
    tags=['Administration'],
    dependencies=[Depends(get_db)],
    responses={404: {"Description": "Not Found"}}
)

def check_admin(token: str, db: Session):
    auth_admin = admin_tool.admin_identification_check(token=token, db=db)
    if not auth_admin:
        raise HTTPException(status_code=400, detail="Permission Denied.")
    return auth_admin

@admin_auth_router.get("/admin_authentication")
def api_admin_auth(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)) -> dict:
    """
    Provide an authentication to administrators for entrance to the Management Web Page.
    :param token: The token of user
    :param db: Database Session.
    :return:
    """
    auth_admin = admin_tool.admin_identification_check(db=db, token=token)
    if not auth_admin:
        raise HTTPException(
            status_code=400,
            detail="Permission Denied."
        )
    return {
        "Code": 200,
        "Administrator": auth_admin.user_name,
        "Status": "Permission Accessed!"
    }

@admin_auth_router.get('/users', response_model=List[schemas.UserAdminView])
def get_all_users(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    return crud.admin_get_all_users(db)

@admin_auth_router.post('/users', response_model=schemas.UserAdminView)
def create_user(user: schemas.UserCreate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    return crud.admin_create_user(db, user)

@admin_auth_router.put('/users/{user_uuid}', response_model=schemas.UserAdminView)
def update_user(user_uuid: str, user: schemas.UserUpdate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    updated_user = crud.admin_update_user(db, user_uuid, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(schemas.UserAdminView.from_orm(updated_user))

@admin_auth_router.delete('/users/{user_uuid}')
def delete_user(user_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    if crud.admin_delete_user(db, user_uuid):
        return {"status": "success", "message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@admin_auth_router.put('/users/{user_uuid}/avatar')
async def update_user_avatar(
    user_uuid: str, 
    avatar: UploadFile = File(...), 
    token: str = Depends(oauth2Scheme), 
    db: Session = Depends(get_db)
):
    check_admin(token, db)
    avatar_path = Path(config.AVATAR_DIR)
    file_suffix = avatar.filename.split(".")[-1]
    
    if not dir_tool.save_user_avatar(user_uuid=user_uuid, avatar=avatar, file_suffix=file_suffix, avatar_path=avatar_path):
        raise HTTPException(status_code=500, detail="Failed to save avatar")
    
    updated_user = crud.admin_get_user_by_uuid(db, user_uuid)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    avatar_url = dir_tool.get_avatar_file_url(user_uuid)[0]
    updated_user['avatar'] = avatar_url  # Change this line
    
    return jsonable_encoder(schemas.UserAdminView(**updated_user))

@admin_auth_router.get('/posts', response_model=List[schemas.PostAdminView])
def get_all_posts(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    posts = crud.admin_get_all_posts(db)
    posts_with_image_links = []
    for post in posts:
        post_dict = post.__dict__
        post_dict['image_link'] = dir_tool.get_post_image_link(post.post_uuid)
        posts_with_image_links.append(post_dict)
    return [schemas.PostAdminView(**post) for post in posts_with_image_links]

@admin_auth_router.post('/posts', response_model=schemas.PostAdminView)
def create_post(post: schemas.PostCreate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    auth_admin = check_admin(token, db)
    return crud.admin_create_post(db, post, auth_admin.user_name)

@admin_auth_router.put('/posts/{post_uuid}', response_model=schemas.PostAdminView)
def update_post(post_uuid: str, post: schemas.PostUpdate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    updated_post = crud.admin_update_post(db, post_uuid, post)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return schemas.PostAdminView(**updated_post)

@admin_auth_router.delete('/posts/{post_uuid}')
def delete_post(post_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    if crud.admin_delete_post(db, post_uuid):
        return {"status": "success", "message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")

@admin_auth_router.get('/comments', response_model=List[schemas.CommentAdminView])
def get_all_comments(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    return crud.admin_get_all_comments(db)

@admin_auth_router.post('/comments', response_model=schemas.CommentAdminView)
def create_comment(comment: schemas.CommentCreate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    auth_admin = check_admin(token, db)
    return crud.admin_create_comment(db, comment, auth_admin.user_name)

@admin_auth_router.put('/comments/{comment_uuid}', response_model=schemas.CommentAdminView)
def update_comment(comment_uuid: str, comment: schemas.CommentUpdate, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    return crud.admin_update_comment(db, comment_uuid, comment)

@admin_auth_router.delete('/comments/{comment_uuid}')
def delete_comment(comment_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    if crud.admin_delete_comment(db, comment_uuid):
        return {"status": "success", "message": "Comment deleted"}
    raise HTTPException(status_code=404, detail="Comment not found")

@admin_auth_router.get('/comments/{comment_uuid}', response_model=schemas.CommentAdminView)
def get_comment(comment_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    comment = crud.admin_get_comment_by_uuid(db, comment_uuid)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@admin_auth_router.get('/user_tendency_addition')
def get_user_tendency(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the tendency of the users in 360 days.
    :param token: The token of the administrator.
    :param db: The Session of the database.
    :return: The data of the users' tendency.
    """
    check_admin(token, db)
    data_final = admin_tool.get_the_tendency_data(db=db)
    x_date = data_final.index.to_list()
    y_user = data_final['users'].to_list()
    y_posts = data_final['posts'].to_list()
    y_comments = data_final['comments'].to_list()
    y_replies = data_final['replies'].to_list()
    chart_tendency = (
        Line()
        .add_xaxis(x_date)
        .add_yaxis('Users', y_user, is_smooth=True)
        .add_yaxis('Posts', y_posts, is_smooth=True)
        .add_yaxis('Comments', y_comments, is_smooth=True)
        .add_yaxis('Replies', y_replies, is_smooth=True)
        .set_global_opts(title_opts=opts.TitleOpts(title="Data tendency"))
    )
    return chart_tendency.dump_options_with_quotes()

@admin_auth_router.get('/posts_toplist')
def get_posts_tops(token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    """
    Get the toplist of the posts by likes.
    :param token: The token of the administrator.
    :param db: The Session of the database.
    :return: The data of the users' tendency.
    """
    check_admin(token, db)
    data_final = admin_tool.get_the_toplist_data(db=db)
    x_axis = data_final['post_title'].to_list()
    y_axis = data_final['dots'].to_list()
    chart_toplist = (
        Funnel()
        .add('Rank by Likes', [list(z) for z in zip(x_axis, y_axis)])
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
            title_opts=opts.TitleOpts(title="Rank"))
    )
    return chart_toplist.dump_options_with_quotes()

@admin_auth_router.get('/users/{user_uuid}', response_model=schemas.UserAdminView)
def get_user(user_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    user = crud.admin_get_user_by_uuid(db, user_uuid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return jsonable_encoder(schemas.UserAdminView(**user))

@admin_auth_router.get('/posts/{post_uuid}', response_model=schemas.PostAdminView)
def get_post(post_uuid: str, token: str = Depends(oauth2Scheme), db: Session = Depends(get_db)):
    check_admin(token, db)
    post = crud.admin_get_post_by_uuid(db, post_uuid)
    if post is None:
        return JSONResponse(status_code=404, content={"detail": "Post not found"})
    
    return schemas.PostAdminView(**post)