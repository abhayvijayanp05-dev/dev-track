from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import Connection

from database import get_db

from model import (
    UserCreate,
    UserResponse,
    TokenResponse
)

from services.auth_service import (
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
        user.password
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