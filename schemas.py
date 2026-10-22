from datetime import date
from pydantic import BaseModel, Field, EmailStr, field_validator


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    dob: date
    email: EmailStr
    course: str = Field(min_length=2, max_length=100)

    @field_validator("name", "course")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be blank")
        return value
