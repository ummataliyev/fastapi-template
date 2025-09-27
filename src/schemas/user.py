"""
User Scheme
"""

from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class UserBase(BaseModel):
    """
    Base schema shared by create and read schemas for User.

    Attributes:
        name (str): Name of the user.
    """
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Inherits:
        - UserBase: Provides `name` field.

    Usage:
        Use this schema to validate incoming data when creating a user.
    """
    pass


class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.

    All fields are optional, allowing partial updates.

    Attributes:
        name (Optional[str]): Updated name of the user, if provided.
    """
    name: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserRead(UserBase):
    """
    Schema for reading user data from the API.

    Attributes:
        id (int): Unique identifier of the user.
        created_at (datetime): Timestamp when the user was created.
        updated_at (datetime): Timestamp when the user was last updated.
    """
    id: int
    created_at: datetime
    updated_at: datetime
