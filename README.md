# FastAPI with SQLAlchemy - Complete Database Example

This project demonstrates a complete database implementation using FastAPI and SQLAlchemy with CRUD operations, relationships, and best practices.

## Project Structure

```
databasewithsqlalchemy/
    main.py              # FastAPI application with all endpoints
    database.py          # Database configuration and session management
    models.py            # SQLAlchemy models (User, Post)
    schemas.py           # Pydantic schemas for request/response validation
    crud.py              # CRUD operations and database queries
    init_db.py           # Database initialization script
    requirements.txt     # Python dependencies
    .env                 # Environment variables
    README.md           # This file
```

## Features Implemented

### 1. Dependencies & Setup
- SQLAlchemy 2.0+ with modern ORM features
- FastAPI with dependency injection
- Pydantic for data validation
- SQLite database (easily switchable to PostgreSQL/MySQL)

### 2. Database Models
- **User Model**: id, username, email, full_name, is_active, timestamps
- **Post Model**: id, title, content, is_published, timestamps, author_id (foreign key)
- **Relationships**: One-to-many relationship between Users and Posts

### 3. CRUD Operations
- **Users**: Create, Read (all/by ID), Update, Delete, Search
- **Posts**: Create, Read (all/by ID/by author/published), Update, Delete, Search

### 4. API Endpoints

#### User Endpoints
- `POST /users/` - Create a new user
- `GET /users/` - Get all users (with pagination)
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user
- `GET /users/search/` - Search users by username, email, or name

#### Post Endpoints
- `POST /posts/` - Create a new post
- `GET /posts/` - Get all posts (with author details)
- `GET /posts/{post_id}` - Get a specific post
- `PUT /posts/{post_id}` - Update a post
- `DELETE /posts/{post_id}` - Delete a post
- `GET /posts/published/` - Get only published posts
- `GET /posts/author/{author_id}` - Get posts by specific author
- `GET /posts/search/` - Search posts by title or content

## Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Setup
Copy `.env` file and configure your database URL:
```bash
# For SQLite (default)
DATABASE_URL=sqlite:///./test.db

# For PostgreSQL
DATABASE_URL=postgresql://user:password@localhost/dbname

# For MySQL
DATABASE_URL=mysql://user:password@localhost/dbname
```

### 3. Initialize Database
```bash
python init_db.py
```

### 4. Run the Application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Common Python Environment Problems & Solutions

### Problem 1: ModuleNotFoundError
**Solution**: Ensure all dependencies are installed and you're in the correct virtual environment.

### Problem 2: Database Connection Issues
**Solution**: Check your DATABASE_URL in .env file and ensure database server is running.

### Problem 3: Port Already in Use
**Solution**: Change the port in main.py or kill the process using the port.

### Problem 4: Permission Issues
**Solution**: Run with appropriate permissions or use a virtual environment.

## Example Usage

### Create a User
```bash
curl -X POST "http://localhost:8000/users/" \
-H "Content-Type: application/json" \
-d '{
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe"
}'
```

### Create a Post
```bash
curl -X POST "http://localhost:8000/posts/" \
-H "Content-Type: application/json" \
-d '{
  "title": "My First Post",
  "content": "This is the content of my first post",
  "author_id": 1
}'
```

### Get All Posts
```bash
curl "http://localhost:8000/posts/"
```

## Database Relationships

This project demonstrates:
- **One-to-Many**: One user can have multiple posts
- **Foreign Keys**: Posts reference users through author_id
- **Lazy Loading**: Relationships are loaded when accessed
- **Cascade Operations**: Deleting a user doesn't delete posts (can be configured)

## Best Practices Implemented

1. **Dependency Injection**: Database sessions managed by FastAPI
2. **Error Handling**: Proper HTTP status codes and error messages
3. **Validation**: Pydantic schemas for request/response validation
4. **Separation of Concerns**: Models, schemas, and CRUD operations in separate files
5. **Pagination**: Skip and limit parameters for list endpoints
6. **Search Functionality**: Full-text search capabilities
7. **Timestamps**: Automatic created_at and updated_at fields
8. **Environment Configuration**: Database URL configurable via environment variables

## Testing the API

Use the interactive Swagger UI at `http://localhost:8000/docs` to test all endpoints, or use curl/postman for manual testing.

## Next Steps

1. Add authentication and authorization
2. Implement database migrations with Alembic
3. Add unit tests
4. Implement caching
5. Add logging and monitoring
6. Deploy to production
