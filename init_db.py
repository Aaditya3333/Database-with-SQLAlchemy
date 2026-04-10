"""
Database initialization script
Run this script to create the database tables
"""
from database import engine, Base
from models import User, Post

def init_db():
    """Initialize the database with all tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
