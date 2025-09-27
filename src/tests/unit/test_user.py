"""
Unit tests for UserService
"""

import pytest
import pytest_asyncio

from unittest.mock import patch
from unittest.mock import AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.services.user import UserService


@pytest.mark.asyncio
class TestUserService:
    @pytest_asyncio.fixture(autouse=True)
    async def setup(self):
        """
        Setup the UserService instance with a mocked AsyncSession for each test.

        :return: None
        """
        self.mock_db = AsyncMock(spec=AsyncSession)
        self.service = UserService(db=self.mock_db)

    async def test_create_user(self):
        """
        Test that UserService.create correctly calls repository.create 
        and returns a User object.

        :return: None
        """
        user_data = {"id": 1, "name": "testuser", "email": "test@example.com"}
        mock_user = User(**user_data)

        with patch.object(
            self.service.repository, "create", AsyncMock(return_value=mock_user)
        ) as mock_create:
            result = await self.service.create(**user_data)
            mock_create.assert_awaited_once_with(obj_in=user_data)
            assert result.id == 1
            assert result.name == "testuser"
            assert result.email == "test@example.com"

    async def test_get_user_by_id(self):
        """
        Test that UserService.get_by_id correctly calls repository.get
        and returns the expected User object.

        :return: None
        """
        mock_user = User(id=1, name="testuser", email="test@example.com")

        with patch.object(
            self.service.repository, "get", AsyncMock(return_value=mock_user)
        ) as mock_get:
            result = await self.service.get_by_id(1)
            mock_get.assert_awaited_once_with(id=1)
            assert result.name == "testuser"

    async def test_update_user(self):
        """
        Test that UserService.update correctly calls repository.update
        with the correct parameters and returns the updated User object.

        :return: None
        """
        updated_data = {"name": "updateduser"}

        with patch.object(
            self.service.repository,
            "update",
            AsyncMock(return_value=User(id=1, name="updateduser", email="test@example.com"))
        ) as mock_update:
            result = await self.service.update(1, **updated_data)
            mock_update.assert_awaited_once()
            called_kwargs = mock_update.call_args[1]
            assert called_kwargs["obj_in"] == updated_data
            assert result.name == "updateduser"

    async def test_delete_user(self):
        """
        Test that UserService.delete correctly calls repository.delete
        and returns the expected success message.

        :return: None
        """
        with patch.object(
            self.service.repository,
            "delete",
            AsyncMock(return_value=None)
        ) as mock_delete:
            result = await self.service.delete(1)
            mock_delete.assert_awaited_once_with(id=1)
            assert result == {"message": "User with id 1 deleted successfully"}
