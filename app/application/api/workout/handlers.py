from application.api.auth.utils import get_current_user
from application.api.workout.schemas import (CreateWorkoutSchema,
                                             DeleteWorkoutResponseSchema,
                                             DeleteWorkoutSchema,
                                             EditWorkoutSchema,
                                             UploadWorkoutFileSchema,
                                             WorkoutDetailSchema)
from domain.entities.user import User
from domain.exceptions.base import ApplicationException
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from logic.commands.workout import (CreateWorkoutCommand, DeleteWorkoutCommand,
                                    EditWorkoutCommand, UploadWorkoutCommand)
from logic.exceptions.auth import AuthException
from logic.exceptions.user import NotFoundException
from logic.mediator.base import Mediator
from punq import Container

router = APIRouter()


@router.post(
    path='/',
    description='Create workout',
    status_code=status.HTTP_201_CREATED,
    response_model=WorkoutDetailSchema,
)
async def create_workout(
        schema: CreateWorkoutSchema,
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> WorkoutDetailSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        workout, *_ = await mediator.handle_command(
            CreateWorkoutCommand(
                email=user.email.as_generic_type(),
                title=schema.title,
                description=schema.description,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return WorkoutDetailSchema.from_entity(workout=workout)


@router.delete(
    path='/',
    description='Delete workout',
    status_code=status.HTTP_200_OK,
    response_model=DeleteWorkoutResponseSchema,
)
async def delete_workout(
        schema: DeleteWorkoutSchema,
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> DeleteWorkoutResponseSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        await mediator.handle_command(
            DeleteWorkoutCommand(
                email=user.email.as_generic_type(),
                workout_id=schema.workout_id,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return DeleteWorkoutResponseSchema()


@router.put(
    path='/add-file',
    description='Upload workout file.',
    status_code=status.HTTP_200_OK,
    response_model=WorkoutDetailSchema,
)
async def upload_workout_file(
        schema: UploadWorkoutFileSchema = Depends(),
        file: UploadFile = File(...),
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> WorkoutDetailSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        workout, *_ = await mediator.handle_command(
            UploadWorkoutCommand(
                workout_id=schema.workout_id,
                email=user.email.as_generic_type(),
                file=file.file,
                file_name=file.filename,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return WorkoutDetailSchema.from_entity(workout=workout)


@router.put(
    path='/',
    description='Edit workout.',
    status_code=status.HTTP_200_OK,
    response_model=WorkoutDetailSchema,
)
async def edit_workout(
        schema: EditWorkoutSchema,
        user: User = Depends(get_current_user),
        container: Container = Depends(),
) -> WorkoutDetailSchema:
    mediator: Mediator = container.resolve(Mediator)
    try:
        workout, *_ = await mediator.handle_command(
            EditWorkoutCommand(
                workout_id=schema.workout_id,
                email=user.email.as_generic_type(),
                title=schema.title,
                description=schema.description,
            )
        )

    except AuthException as auth_error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': auth_error.message})

    except NotFoundException as not_found_error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': not_found_error.message})

    except ApplicationException as app_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': app_error.message})

    return WorkoutDetailSchema.from_entity(workout=workout)
