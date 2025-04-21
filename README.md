# Management API

A FastAPI application for managing books and users with PostgreSQL database backend.

## Features

- **User Management**:
  - Create users with unique usernames and emails
  - Update user information
  - Password hashing for security

- **Book Management**:
  - Add new book
  - Update book details
  - Change book ownership (user_id)
  - Unique title enforcement

- **Movies Management**:
  - Add new movie
  - Update movie details
  - Change movie ownership (user_id)
  - Unique title enforcement
  
- **Board Games Management**:
  - Add new board game
  - Update game details
  - Change game ownership (user_id)
  - Unique title enforcement
  
- **Comics Management**:
  - Add new comic
  - Update comic details
  - Change comic ownership (user_id)
  - Unique title enforcement

- **Database**:
  - Async PostgreSQL with SQLAlchemy ORM
  - Alembic for database migrations
  - Proper session management

## Technologies Used

- Python 3.9+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic (for migrations)
- Pydantic (for data validation)
- asyncpg (PostgreSQL async driver)

## Installation

### Prerequisites

- Python 3.9 or higher
- PostgreSQL server
- pip package manager

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/book-management-api.git
   cd book-management-api
   
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
4. Set up the environment variables:
   Create a `.env` file in the root directory with the following content:
   ```env
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
   ```

5. Set up the database:
   ```bash
   # Create the database (run in psql)
    CREATE DATABASE bookdb;
    
    # Run migrations
    alembic upgrade head
   ```
   
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
   
## Postman Testing Guide

### 1. User Creation
**Request:**
```http
    POST http://127.0.0.1:8000/users
    Content-Type: application/json
    
    {
      "name": "John Doe",
      "username": "johndoe",
      "email": "john@example.com",
      "password": "password123",
      "role": "user"
    }
```
**Request:**
```http
    PUT http://127.0.0.1:8000/users
    Content-Type: application/json
    
    {
      "username": "john_doe",
      "role": "admin"
    }
```
### 2. Book Creation
**Request:**
```http
    POST http://127.0.0.1:8000/books
    Content-Type: application/json
    
    {
      "title": "Python Programming",
      "author": "Author Name",
      "genre": "Fiction",
      "published_date": "2023-01-01",
      "rating": 4,
      "user_id": 1
    }
```
**Request:**
```http
    PUT http://127.0.0.1:8000/books
    Content-Type: application/json
    
    {
      "title": "Test book",
      "genre": "Drama",
    }
```
### 3. Movie Creation
**Request:**
```http
    POST http://127.0.0.1:8000/movies
    Content-Type: application/json
    
    {
      "title": "Jurassic Park",
      "director": "Author Name",
      "genre": "Action",
      "release_date": "2023-01-01",
      "rating": 4,
      "user_id": 1
    }
```
**Request:**
```http
    PUT http://127.0.0.1:8000/movies
    Content-Type: application/json
    
    {
      "title": "Test book",
      "genre": "Drama",
    }
```
### 4. Board Game Creation
**Request:**
```http
    POST http://127.0.0.1:8000/board_games
    Content-Type: application/json
    
    {
      "title": "Sample Game",
      "designer": "Mehmet",
      "genre": "Fiction",
      "release_date": "2023-01-01",
      "user_id": 1
    }
```
**Request:**
```http
    PUT http://127.0.0.1:8000/board_games
    Content-Type: application/json
    
    {
      "title": "Test Game",
      "genre": "Action",
    }
```
### 4. Comics Creation
**Request:**
```http
    POST http://127.0.0.1:8000/comics
    Content-Type: application/json
    
    {
      "title": "Sample Comic",
      "author": "Mehmet",
      "genre": "Fiction",
      "published_date": "2023-01-01",
      "user_id": 1
    }
```
**Request:**
```http
    PUT http://127.0.0.1:8000/comics
    Content-Type: application/json
    
    {
      "title": "Test Comic",
      "genre": "Drama",
    }
```