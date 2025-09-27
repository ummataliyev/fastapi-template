"""
User Table
"""

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.storage.postgres import Base
from db.storage.postgres.mixins import IntIdPkMixin
from db.storage.postgres.mixins import TimestampMixin
from db.storage.postgres.mixins import SoftDeletionMixin


class User(Base, IntIdPkMixin, TimestampMixin, SoftDeletionMixin):
    """
    SQLAlchemy model representing a user.
    """
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)

    def __repr__(self) -> str:
        """
        Return a readable string representation of the User instance.
        """
        return f"<User id={self.id} name={self.name} email={self.email}>"
