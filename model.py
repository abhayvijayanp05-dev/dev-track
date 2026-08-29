from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    pending = "pending"


class ProjectCreate(BaseModel):
    id: int = Field(gt=0)
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

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str