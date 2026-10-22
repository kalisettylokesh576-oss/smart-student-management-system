from fastapi import FastAPI, HTTPException, Query
import sqlite3

from app.database import get_connection, init_db
from app.schemas import StudentCreate

app = FastAPI(
    title="Smart Student Management System",
    description="Student CRUD API using FastAPI and SQLite",
    version="1.0.0"
)

init_db()


@app.get("/")
def home():
    return {"message": "Smart Student Management API is running"}


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    data = student.model_dump(mode="json")
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """INSERT INTO students (name, dob, email, course)
                   VALUES (?, ?, ?, ?)""",
                (data["name"], data["dob"], data["email"], data["course"])
            )
            return {
                "message": "Student created successfully",
                "student_id": cursor.lastrowid
            }
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists"
        )


@app.get("/search/students")
def search_students(
    name: str | None = Query(default=None, min_length=1),
    course: str | None = Query(default=None, min_length=1)
):
    if name is None and course is None:
        raise HTTPException(
            status_code=400,
            detail="Provide a name or course to search"
        )

    sql = "SELECT * FROM students WHERE 1=1"
    params = []

    if name:
        sql += " AND name LIKE ?"
        params.append(f"%{name}%")
    if course:
        sql += " AND course LIKE ?"
        params.append(f"%{course}%")

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
        return {"count": len(rows), "students": [dict(r) for r in rows]}


@app.get("/students")
def get_students():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
        return {"count": len(rows), "students": [dict(r) for r in rows]}


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentCreate):
    data = student.model_dump(mode="json")
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """UPDATE students
                   SET name = ?, dob = ?, email = ?, course = ?
                   WHERE id = ?""",
                (data["name"], data["dob"], data["email"],
                 data["course"], student_id)
            )
            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404, detail="Student not found"
                )
            return {"message": "Student updated successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A student with this email already exists"
        )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM students WHERE id = ?", (student_id,)
        )
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404, detail="Student not found"
            )
        return {"message": "Student deleted successfully"}
