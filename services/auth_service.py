from repositories.user_repository import (
    create_user,
    get_user_by_email
)
from auth.security import (
    hash_password,
    verify_password,
    create_access_token
)

def register_user(
    connection,
    email: str,
    password: str,
    role: str,
    status: str
):
    hashed_password = hash_password(password)

    user = create_user(
        connection,
        email,
        hashed_password,
        role,
        status
    )

    return {
        "id": user[0],
        "email": user[1],
        "role": user[2],
        "status": user[3]
    }



# *************************************************************
def login_user(
    connection,
    email: str,
    password: str
):
    user = get_user_by_email(
        connection,
        email
    )

    if user is None:
        return None

    password_is_valid = verify_password(
        password,
        user[2]
    )

    if not password_is_valid:
        return None

    access_token = create_access_token(
        data={
            "sub": str(user[0]),
            "email": user[1],
            "role": user[3]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }