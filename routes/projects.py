from fastapi import APIRouter, Depends, HTTPException
from psycopg import Connection

from auth.dependencies import get_current_user
from auth.authorization import require_roles
from database import get_db

from model import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    ProjectMessageResponse
)

from services.project_service import (
    get_all_projects_service,
    get_project,
    create_project_service,
    update_project_service,
    delete_project_service
)

from exceptions import (
    ProjectAlreadyExistsError,
    ProjectNotFoundError,
    ProjectForbiddenError
)


router = APIRouter()


@router.get("/")
def greet():
    return "DevTrack API is running 🚀"


@router.get(
    "/projects",
    response_model=ProjectListResponse
)
def get_all_projects_route(
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_all_projects_service(connection)

@router.post(
    "/projects",
    status_code=201,
    response_model=ProjectMessageResponse
)
def create_project_route(
    project: ProjectCreate,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(require_roles("teacher", "admin"))
):
    try:
        created_project = create_project_service(
            connection,
            project.name,
            project.status,
            current_user
        )
    except ProjectAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Project already exists"
        )

    return {
        "message": "Project created successfully",
        "project": created_project
    }


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse
)
def get_project_route(
    project_id: int,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        return get_project(
            connection,
            project_id
        )

    except ProjectNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

@router.put(
    "/projects/{project_id}",
    response_model=ProjectMessageResponse
)
def update_project_route(
    project_id: int,
    updated_project: ProjectUpdate,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(
        require_roles("teacher", "admin")
    )
):
    try:
        project = update_project_service(
            connection,
            project_id,
            updated_project.name,
            updated_project.status,
            current_user
        )

    except ProjectNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    except ProjectForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to modify this project"
        )

    return {
        "message": "Project updated successfully",
        "project": project
    }


@router.delete(
    "/projects/{project_id}",
    status_code=204
)
def delete_project_route(
    project_id: int,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(
        require_roles("teacher", "admin")
    )
):
    try:
        delete_project_service(
            connection,
            project_id,
            current_user
        )

    except ProjectNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    except ProjectForbiddenError:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this project"
        )

    return