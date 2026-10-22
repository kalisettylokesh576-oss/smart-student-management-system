# Smart Student Management System

A student CRUD REST API built using Python, FastAPI, Pydantic, and SQLite.

## Features
- Create, read, update, and delete student records
- Search by student name or course
- Email, date, and text validation
- Duplicate email protection
- HTTP error handling
- Interactive API documentation

## Requirements
Python 3.10 or newer.

## Installation
```bash
python -m venv .venv
```

Activate the environment, then run:
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to explore the API.

## API endpoints
- POST /students
- GET /students
- GET /students/{student_id}
- PUT /students/{student_id}
- DELETE /students/{student_id}
- GET /search/students?name=Rahul
- GET /search/students?course=CSE

## Database
SQLite creates the students database automatically.

## Testing
Run `pytest -v` from the project directory after adding the test file.
