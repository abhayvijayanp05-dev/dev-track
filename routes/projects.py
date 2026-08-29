from fastapi import APIRouter, Depends, HTTPException
from auth.dependencies import get_current_user
from psycopg import Connection
from auth.authorization import require_roles
from database import get_db
# from repositories.project_repository import (
#     get_all_projects,
#     # create_project,
#     # get_project_by_id,
#     # update_project,
#     # delete_project)
from model import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse

)

from services.project_service import (
    get_all_projects_service,
    get_project,
    create_project_service,
    update_project_service,
    delete_project_service
)


from auth.dependencies import get_current_user



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



#post some data inside of the data base 


@router.post("/projects", status_code=201)
def create_project_route(
    project: ProjectCreate,
    connection: Connection = Depends(get_db),
    current_user: dict = Depends(require_roles("teacher", "admin"))
):
    created_project = create_project_service(
        connection,
        project.id,
        project.name,
        project.status
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
    return get_project(
        connection,
        project_id
    )


@router.put("/projects/{project_id}")
def update_project_route(
    project_id: int,
    updated_project: ProjectUpdate,
    connection: Connection = Depends(get_db),
     current_user: dict = Depends(
            require_roles("teacher", "admin")
        )

):
    project = update_project_service(
        connection,
        project_id,
        updated_project.name,
        updated_project.status
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
        require_roles("admin")
    )
):
    deleted = delete_project_service(
        connection,
        project_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return

# DELETE /api/projects/1
#           │
#           ▼
#    projects.py
#           │
#           ▼
# delete_project_service()
#           │
#           ├── get_project_by_id()
#           │       │
#           │       ▼
#           │   PostgreSQL
#           │
#           └── delete_project()
#                   │
#                   ▼
#               PostgreSQL