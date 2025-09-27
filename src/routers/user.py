"""
User Routers
"""

from fastapi import status
from fastapi import Depends
from fastapi import APIRouter

from src.schemas.user import UserCreate
from src.schemas.user import UserUpdate

from src.services.user import UserService
from src.response.user import UserResponse
from src.interfaces.scheme import BaseScheme


router = APIRouter()
response = UserResponse()


@router.get(
    path="/{id}",
    response_model=BaseScheme
)
async def get_user_by_id(
    id: int,
    service: UserService = Depends(UserService.get_service)
):
    """
    Retrieve a single user by ID.

    :param id: ID of the user to retrieve.
    :param service: UserService instance injected by FastAPI Depends.
    :return: Standardized BaseScheme response containing the user or error.
    """
    try:
        user = await service.get_by_id(id)
        return response.get_user(user)
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.error(f"An error occurred: {e}")


@router.get(
    path="/",
    response_model=BaseScheme
)
async def get_all_users(
    service: UserService = Depends(UserService.get_service)
):
    """
    Retrieve all users.

    :param service: UserService instance injected by FastAPI Depends.
    :return: Standardized BaseScheme response containing list of users or error.
    """
    try:
        users = await service.get_all()
        return response.get_all(users)
    except Exception as e:
        return response.error(f"An error occurred: {e}")


@router.post(
    path="/",
    response_model=BaseScheme,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(UserService.get_service)
):
    """
    Create a new user.

    :param user_in: UserCreate schema containing input data.
    :param service: UserService instance injected by FastAPI Depends.
    :return: Standardized BaseScheme response with the created user or error.
    """
    try:
        new_user = await service.create(**user_in.model_dump())
        return response.create(new_user)
    except Exception as e:
        return response.error(f"An error occurred: {e}")


@router.patch(
    path="/{id}",
    response_model=BaseScheme
)
async def update_user(
    id: int,
    user_in: UserUpdate,
    service: UserService = Depends(UserService.get_service)
):
    """
    Update an existing user by ID.

    :param id: ID of the user to update.
    :param user_in: UserUpdate schema containing fields to update.
    :param service: UserService instance injected by FastAPI Depends.
    :return: Standardized BaseScheme response with updated user or error.
    """
    try:
        updated_user = await service.update(
            id,
            **user_in.model_dump(exclude_unset=True)
        )
        return response.update(updated_user)
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.error(f"An error occurred: {e}")


@router.delete(
    path="/{id}",
    response_model=BaseScheme
)
async def delete_user(
    id: int,
    service: UserService = Depends(UserService.get_service)
):
    """
    Delete a user by ID.

    :param id: ID of the user to delete.
    :param service: UserService instance injected by FastAPI Depends.
    :return: Standardized BaseScheme response confirming deletion or error.
    """
    try:
        await service.delete(id)
        return response.delete()
    except ValueError:
        return response.user_not_found()
    except Exception as e:
        return response.error(f"An error occurred: {e}")
