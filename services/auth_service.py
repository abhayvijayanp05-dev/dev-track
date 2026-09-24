from repositories.user_repository import (
    create_user,
    get_user_by_email,
    approve_teacher,
    get_all_users,
    get_all_students
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

    # Check account status
    if user[4] != "active":
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


def approve_teacher_service(
    connection,
    user_id: int
):
    user = approve_teacher(
        connection,
        user_id
    )

    if user is None:
        return None

    return {
        "id": user[0],
        "email": user[1],
        "role": user[2],
        "status": user[3]
    }


def get_all_users_service(connection):
    rows = get_all_users(connection)

    return {
        "users": [
            {
                "id": row[0],
                "email": row[1],
                "role": row[2],
                "status": row[3]
            }
            for row in rows
        ]
    }


def get_all_students_service(connection):
    rows = get_all_students(connection)

    return {
        "students": [
            {
                "id": row[0],
                "email": row[1],
                "role": row[2],
                "status": row[3]
            }
            for row in rows
        ]
    }
