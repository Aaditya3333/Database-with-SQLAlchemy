from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from database import get_db, engine
from models import Base, User, Post
from schemas import UserCreate, UserUpdate, User as UserSchema, PostCreate, PostUpdate, Post as PostSchema, PostWithAuthor
import crud

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI with SQLAlchemy", description="A complete database example")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}

# User endpoints
@app.post("/users/", response_model=UserSchema, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserSchema)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.get("/users/search/", response_model=List[UserSchema])
def search_users(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.search_users(db, query=query, skip=skip, limit=limit)
    return users

# Post endpoints
@app.post("/posts/", response_model=PostSchema, status_code=201)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Check if author exists
    author = crud.get_user(db, user_id=post.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return crud.create_post(db=db, post=post)

@app.get("/posts/", response_model=List[PostWithAuthor])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    # Load author information for each post
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        post_dict['author'] = post.author
        result.append(PostWithAuthor(**post_dict))
    return result

@app.get("/posts/{post_id}", response_model=PostWithAuthor)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_dict = db_post.__dict__.copy()
    post_dict['author'] = db_post.author
    return PostWithAuthor(**post_dict)

@app.put("/posts/{post_id}", response_model=PostSchema)
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id=post_id, post_update=post_update)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    success = crud.delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

@app.get("/posts/published/", response_model=List[PostWithAuthor])
def read_published_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_published_posts(db, skip=skip, limit=limit)
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        post_dict['author'] = post.author
        result.append(PostWithAuthor(**post_dict))
    return result

@app.get("/posts/author/{author_id}", response_model=List[PostWithAuthor])
def read_posts_by_author(author_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Check if author exists
    author = crud.get_user(db, user_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    posts = crud.get_posts_by_author(db, author_id=author_id, skip=skip, limit=limit)
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        post_dict['author'] = post.author
        result.append(PostWithAuthor(**post_dict))
    return result

@app.get("/posts/search/", response_model=List[PostWithAuthor])
def search_posts(query: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.search_posts(db, query=query, skip=skip, limit=limit)
    result = []
    for post in posts:
        post_dict = post.__dict__.copy()
        post_dict['author'] = post.author
        result.append(PostWithAuthor(**post_dict))
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
