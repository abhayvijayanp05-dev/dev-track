from repositories.project_repository import (
    get_all_projects,
    get_project_by_id,
    create_project,
    update_project,
    delete_project
)

from exceptions import (
    ProjectAlreadyExistsError,
    ProjectNotFoundError
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
    project_id: int,
    name: str,
    status: str
):
    try:
        create_project(
            connection,
            project_id,
            name,
            status
        )

    except UniqueViolation:
        raise ProjectAlreadyExistsError()

    return {
        "id": project_id,
        "name": name,
        "status": status
    }

def update_project_service(
    connection,
    project_id: int,
    name: str,
    status: str
):
    # Check whether the project exists
    existing_project = get_project_by_id(
        connection,
        project_id
    )

    if existing_project is None:
     raise ProjectNotFoundError()
    # Update the project
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
    project_id: int
):
    existing_project = get_project_by_id(
        connection,
        project_id
    )

    if existing_project is None:
     raise ProjectNotFoundError()

    delete_project(
        connection,
        project_id
    )

    return True