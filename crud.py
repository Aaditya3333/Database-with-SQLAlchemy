from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models import User, Post
from schemas import UserCreate, UserUpdate, PostCreate, PostUpdate
from typing import Optional, List

# User CRUD operations
def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Post CRUD operations
def get_post(db: Session, post_id: int) -> Optional[Post]:
    return db.query(Post).filter(Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).offset(skip).limit(limit).all()

def get_posts_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).filter(Post.author_id == author_id).offset(skip).limit(limit).all()

def get_published_posts(db: Session, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).filter(Post.is_published == True).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate) -> Post:
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: PostUpdate) -> Optional[Post]:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        update_data = post_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False

# Search functions
def search_users(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).filter(
        or_(
            User.username.ilike(f"%{query}%"),
            User.email.ilike(f"%{query}%"),
            User.full_name.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()

def search_posts(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Post]:
    return db.query(Post).filter(
        or_(
            Post.title.ilike(f"%{query}%"),
            Post.content.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()
