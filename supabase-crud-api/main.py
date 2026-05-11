
# Simple CRUD (create, retrieve, update, delete) Operation in student database using API.
# Supabase connected - Table name (students), name, email, course, created at (timestamp).

# Import libraries
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client

# Loading the environment variables
load_dotenv()

app = FastAPI()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class Student(BaseModel):
    name: str
    email: str
    course: str

# Home URL
@app.get("/")
def home():
    return "Student CRUD operations. API endpoint: /student. Method: get,post,put,delete"

# Push data into database
@app.post("/students")
def create_student(student: Student):
    result = supabase.table("students").insert(student.dict()).execute()
    return result.data

# Retrieve data from database
@app.get("/students")
def get_students():
    result = supabase.table("students").select("*").execute()
    return result.data

# Retrieve student data by id
@app.get("/students/{student_id}")
def get_student(student_id: int):
    result = supabase.table("students").select("*").eq("id", student_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Student not found")

    return result.data[0]

# Updation in student via id parameter
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    result = (
        supabase.table("students")
        .update(student.dict())
        .eq("id", student_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Student not found")

    return result.data[0]

# Deletion of student data by id
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    result = supabase.table("students").delete().eq("id", student_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}