from repositories.project_repository import (
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project
)

from exceptions import (
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
    ProjectForbiddenError
)

from psycopg.errors import UniqueViolation

def get_all_projects_service(connection):
    rows = get_all_projects(connection)

    return {
        "projects": [
            {
                "id": row[0],
                "name": row[1],
                "status": row[2]
            }
            for row in rows
        ]
    }

def get_project(
    connection,
    project_id: int
):
    row = get_project_by_id(
        connection,
        project_id
    )

    if row is None:
     raise ProjectNotFoundError()


    return {
        "id": row[0],
        "name": row[1],
        "status": row[2]
    }

def create_project_service(
    connection,
    name: str,
    status: str,
    current_user: dict
):
    owner_id = current_user["id"]

    try:
        row = create_project(
            connection,
            name,
            status,
            owner_id
        )
    except UniqueViolation:
        raise ProjectAlreadyExistsError()

    return {
        "id": row[0],
        "name": row[1],
        "status": row[2]
    }

def update_project_service(
    connection,
    project_id: int,
    name: str,
    status: str,
    current_user: dict
):
    existing_project = get_project_by_id(
        connection,
        project_id
    )

    if existing_project is None:
        raise ProjectNotFoundError()

    owner_id = existing_project[3]

    user_id = current_user["id"]
    user_role = current_user["role"]

    # Admin can update any project
    if user_role != "admin" and user_id != owner_id:
        raise ProjectForbiddenError()

    update_project(
        connection,
        project_id,
        name,
        status
    )

    return {
        "id": project_id,
        "name": name,
        "status": status
    }
def delete_project_service(
    connection,
    project_id: int,
    current_user: dict
):
    existing_project = get_project_by_id(
        connection,
        project_id
    )

    if existing_project is None:
        raise ProjectNotFoundError()


    owner_id = existing_project[3]

    user_id = current_user["id"]
    user_role = current_user["role"]

    # Admin can delete any project
    if user_role != "admin" and user_id != owner_id:
        raise ProjectForbiddenError()

    delete_project(
        connection,
        project_id
    )

    return True