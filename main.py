
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from routes.projects import router as project_router
from routes.auth import router as auth_router
from fastapi.encoders import jsonable_encoder

from exceptions import (
    ProjectAlreadyExistsError,
    ProjectNotFoundError
)


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        error = error.copy()

        if isinstance(error.get("input"), bytes):
            error["input"] = "<request body omitted>"

        errors.append(error)

    return JSONResponse(
        status_code=422,
        content={
            "detail": errors
        }
    )

@app.exception_handler(ProjectNotFoundError)
async def project_not_found_handler(
    request: Request,
    exc: ProjectNotFoundError
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Project not found"
        }
    )


@app.exception_handler(ProjectAlreadyExistsError)
async def project_already_exists_handler(
    request: Request,
    exc: ProjectAlreadyExistsError
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Project already exists"
        }
    )


app.include_router(
    project_router,
    prefix="/api",
    tags=["Projects"]
)



# projects = [Project(id=1, name="MentorLoop", status="completed"),
#              Project(id=2, name="DevTrack", status="in progress")]


#  get all project friom the data base 


app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Authentication"]
)