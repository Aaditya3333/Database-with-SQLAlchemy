"""
Simple Flask-like app using basic Python HTTP server
This bypasses the FastAPI/Pydantic compatibility issues
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
from urllib.parse import urlparse, parse_qs
import threading
import time

class DatabaseHandler:
    def __init__(self):
        self.conn = sqlite3.connect('test.db', check_same_thread=False)
        self.init_db()
    
    def init_db(self):
        cursor = self.conn.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Create posts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                is_published BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                author_id INTEGER,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
        ''')
        self.conn.commit()
    
    def get_users(self, skip=0, limit=100):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, skip))
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    
    def create_user(self, username, email, full_name=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, full_name) 
            VALUES (?, ?, ?)
        ''', (username, email, full_name))
        self.conn.commit()
        return {"id": cursor.lastrowid, "username": username, "email": email, "full_name": full_name}
    
    def get_posts(self, skip=0, limit=100):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT p.*, u.username, u.email 
            FROM posts p 
            LEFT JOIN users u ON p.author_id = u.id 
            LIMIT ? OFFSET ?
        ''', (limit, skip))
        return [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    
    def create_post(self, title, content, author_id, is_published=False):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO posts (title, content, author_id, is_published) 
            VALUES (?, ?, ?, ?)
        ''', (title, content, author_id, is_published))
        self.conn.commit()
        return {"id": cursor.lastrowid, "title": title, "content": content, "author_id": author_id}

db = DatabaseHandler()

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"message": "Database API is running!", "endpoints": ["/users", "/posts"]}
            self.wfile.write(json.dumps(response).encode())
        
        elif self.path == '/users':
            users = db.get_users()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(users).encode())
        
        elif self.path == '/posts':
            posts = db.get_posts()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(posts).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/users':
                user = db.create_user(
                    username=data.get('username'),
                    email=data.get('email'),
                    full_name=data.get('full_name')
                )
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(user).encode())
            
            elif self.path == '/posts':
                post = db.create_post(
                    title=data.get('title'),
                    content=data.get('content'),
                    author_id=data.get('author_id'),
                    is_published=data.get('is_published', False)
                )
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(post).encode())
            
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')
        
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run_server():
    server = HTTPServer(('localhost', 8000), APIHandler)
    print("Server running at http://localhost:8000")
    print("Available endpoints:")
    print("  GET  /")
    print("  GET  /users")
    print("  POST /users")
    print("  GET  /posts")
    print("  POST /posts")
    print("\nExample usage:")
    print("curl -X GET http://localhost:8000/users")
    print('curl -X POST http://localhost:8000/users -H "Content-Type: application/json" -d \'{"username": "test", "email": "test@example.com"}\'')
    server.serve_forever()

if __name__ == "__main__":
    run_server()
