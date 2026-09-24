from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import Connection

from auth.authorization import require_roles
from auth.dependencies import get_current_user
from database import get_db

from exceptions import ProjectForbiddenError, ProjectNotFoundError
from model import (
    UserCreate,
    UserListResponse_viewing_by_admin,
    UserListResponse_viewing_by_teacher,
    UserListResponse_viewing_by_teacher,
    UserResponse,
    TokenResponse,
    
)

from services.auth_service import (
    approve_teacher_service,
    get_all_users_service,
    get_all_students_service,
    register_user,
    login_user
)


router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    connection: Connection = Depends(get_db)
):
    return register_user(
    connection,
    user.email,
    user.password,
    "student",
    "active"
)


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    connection: Connection = Depends(get_db)
):
    authenticated_user = login_user(
        connection,
        form_data.username,
        form_data.password
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return authenticated_user




@router.post(
    "/teacher-register",
    response_model=UserResponse,
    status_code=201
)
def teacher_register(
    user: UserCreate,
    connection: Connection = Depends(get_db)
):
    return register_user(
        connection,
        user.email,
        user.password,
        "teacher",
        "pending"
    )

@router.put("/users/{user_id}/approve")
def approve_teacher_route(
    user_id: int,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin")
    )
):
    user = approve_teacher_service(
        connection,
        user_id,
     
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found or already approved"
        )

    return {
        "message": "Teacher approved successfully",
        "user": user
    }
@router.get(
    "/teachers",
    response_model=UserListResponse_viewing_by_admin
)
def get_all_users_route(
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(
        require_roles("admin")
    )
):
    return get_all_users_service(connection)



@router.get(
    "/students",
    response_model=UserListResponse_viewing_by_teacher
)
def get_all_students_route(
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(
        require_roles("teacher", "admin")
    )
):
    return get_all_students_service(connection)