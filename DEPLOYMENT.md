# Deployment Guide - FastAPI SQLAlchemy Database Application

## Overview
This guide covers deploying the FastAPI SQLAlchemy database application to various platforms including GitHub, cloud services, and local production environments.

## Table of Contents
1. [GitHub Repository Setup](#github-repository-setup)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment Options](#cloud-deployment-options)
5. [Environment Configuration](#environment-configuration)
6. [Database Setup](#database-setup)
7. [Production Considerations](#production-considerations)

## GitHub Repository Setup

### 1. Create GitHub Repository
```bash
# Create a new repository on GitHub
# Repository name: fastapi-sqlalchemy-database
# Description: Complete FastAPI application with SQLAlchemy database operations
# Make it Public
# Don't initialize with README (we already have one)
```

### 2. Push to GitHub
```bash
# Add remote repository
git remote add origin https://github.com/yourusername/fastapi-sqlalchemy-database.git

# Push to GitHub
git push -u origin master
```

### 3. GitHub Pages Documentation
The project includes comprehensive documentation that can be deployed to GitHub Pages:
- `docs.html` - Interactive API documentation
- `README.md` - Project documentation
- Swagger UI available at `/docs` when running

## Local Development

### Prerequisites
- Python 3.11+ (recommended Python 3.12)
- Git
- Modern web browser

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/yourusername/fastapi-sqlalchemy-database.git
cd fastapi-sqlalchemy-database

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run the application
python main.py

# Access the application
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
# API: http://localhost:8000
```

## Docker Deployment

### 1. Create Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///./app.db
    volumes:
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=fastapi_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### 3. Build and Run
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run with Docker
docker build -t fastapi-sqlalchemy .
docker run -p 8000:8000 fastapi-sqlalchemy
```

## Cloud Deployment Options

### 1. Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### 2. Render
1. Connect GitHub repository to Render
2. Set environment variables
3. Deploy automatically from GitHub

### 3. Heroku
```bash
# Install Heroku CLI
# Create app
heroku create your-app-name

# Set environment variables
heroku config:set DATABASE_URL=postgresql://user:pass@host/db

# Deploy
git push heroku master
```

### 4. Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Environment Configuration

### Environment Variables (.env)
```bash
# Database Configuration
DATABASE_URL=sqlite:///./test.db
# For PostgreSQL: postgresql://user:password@localhost/dbname
# For MySQL: mysql://user:password@localhost/dbname

# Application Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=["http://localhost:3000", "https://yourdomain.com"]
```

### Production Environment Variables
```bash
# Security
SECRET_KEY=your-very-secure-secret-key
DEBUG=False

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://username:password@host:5432/dbname

# CORS
CORS_ORIGINS=["https://yourdomain.com"]

# Logging
LOG_LEVEL=INFO
```

## Database Setup

### SQLite (Development)
```bash
# Database file is created automatically
# No additional setup required
```

### PostgreSQL (Production)
```bash
# Install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE fastapi_db;
CREATE USER fastapi_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO fastapi_user;
\q

# Update .env file
DATABASE_URL=postgresql://fastapi_user:secure_password@localhost/fastapi_db
```

### Database Migrations
```bash
# Generate migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

## Production Considerations

### 1. Security
- Use strong SECRET_KEY
- Enable HTTPS
- Use environment variables for sensitive data
- Implement authentication (JWT, OAuth)
- Rate limiting
- Input validation

### 2. Performance
- Use PostgreSQL for production
- Implement caching (Redis)
- Database connection pooling
- Load balancing
- CDN for static assets

### 3. Monitoring
- Application logging
- Performance monitoring
- Error tracking (Sentry)
- Health checks
- Database monitoring

### 4. Scaling
- Horizontal scaling with multiple instances
- Database replication
- Microservices architecture
- Container orchestration (Kubernetes)

## API Documentation

### Swagger UI
- Interactive API documentation
- Available at `/docs` when running
- Try out endpoints directly in browser

### ReDoc
- Alternative documentation format
- Available at `/redoc` when running
- More readable documentation

### Custom Documentation
- `docs.html` - Interactive testing interface
- `README.md` - Project documentation
- Inline code documentation

## Testing

### Run Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test
pytest tests/test_users.py
```

### API Testing
```bash
# Test API endpoints
python test_api.py

# Or use curl
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com"}'
```

## Troubleshooting

### Common Issues
1. **Python version compatibility**: Use Python 3.11+
2. **Database connection errors**: Check DATABASE_URL
3. **Import errors**: Ensure all dependencies installed
4. **Port conflicts**: Change port in main.py
5. **Permission errors**: Check file permissions

### Debug Mode
```bash
# Run with debug mode
uvicorn main:app --reload --log-level debug

# Check logs
tail -f app.log
```

## Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Create GitHub Issue
- Check documentation
- Review troubleshooting section
- Contact maintainers

---

**Deployment Status**: Ready for deployment to any platform
**Last Updated**: 2026-04-10
**Version**: 1.0.0
