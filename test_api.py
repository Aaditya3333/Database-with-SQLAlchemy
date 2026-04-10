"""
Test script to demonstrate API functionality
Run this after starting the main.py application
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("Testing FastAPI with SQLAlchemy API...")
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}, Response: {response.json()}")
    
    # Create a user
    print("\n2. Creating a user...")
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User"
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    print(f"Status: {response.status_code}, Response: {response.json()}")
    
    if response.status_code == 201:
        user_id = response.json()["id"]
        print(f"Created user with ID: {user_id}")
        
        # Get all users
        print("\n3. Getting all users...")
        response = requests.get(f"{BASE_URL}/users/")
        print(f"Status: {response.status_code}, Users: {len(response.json())}")
        
        # Get specific user
        print("\n4. Getting specific user...")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(f"Status: {response.status_code}, User: {response.json()}")
        
        # Create a post
        print("\n5. Creating a post...")
        post_data = {
            "title": "My First Post",
            "content": "This is the content of my first post",
            "author_id": user_id
        }
        response = requests.post(f"{BASE_URL}/posts/", json=post_data)
        print(f"Status: {response.status_code}, Response: {response.json()}")
        
        if response.status_code == 201:
            post_id = response.json()["id"]
            print(f"Created post with ID: {post_id}")
            
            # Get all posts
            print("\n6. Getting all posts...")
            response = requests.get(f"{BASE_URL}/posts/")
            print(f"Status: {response.status_code}, Posts: {len(response.json())}")
            
            # Get posts by author
            print("\n7. Getting posts by author...")
            response = requests.get(f"{BASE_URL}/posts/author/{user_id}")
            print(f"Status: {response.status_code}, Posts by author: {len(response.json())}")
            
            # Update post to publish it
            print("\n8. Publishing post...")
            update_data = {"is_published": True}
            response = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
            print(f"Status: {response.status_code}, Response: {response.json()}")
            
            # Get published posts
            print("\n9. Getting published posts...")
            response = requests.get(f"{BASE_URL}/posts/published/")
            print(f"Status: {response.status_code}, Published posts: {len(response.json())}")
            
            # Search functionality
            print("\n10. Testing search...")
            response = requests.get(f"{BASE_URL}/users/search/?query=test")
            print(f"Status: {response.status_code}, Search results: {len(response.json())}")
            
            # Clean up (optional)
            print("\n11. Cleaning up...")
            response = requests.delete(f"{BASE_URL}/posts/{post_id}")
            print(f"Deleted post - Status: {response.status_code}")
            
            response = requests.delete(f"{BASE_URL}/users/{user_id}")
            print(f"Deleted user - Status: {response.status_code}")
    
    print("\nAPI testing completed!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
