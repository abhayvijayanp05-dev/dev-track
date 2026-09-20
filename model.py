from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    pending = "pending"
    rejected = "rejected"


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    status: ProjectStatus


class ProjectUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    status: ProjectStatus


class ProjectResponse(BaseModel):
    id: int
    name: str
    status: ProjectStatus


class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]



class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    status: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ProjectMessageResponse(BaseModel):
    message: str
    project: ProjectResponse