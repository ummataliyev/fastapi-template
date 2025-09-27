"""
Pagination and ID encoding/decoding utilities.
"""

from sqlalchemy import func

from cryptography import fernet

from libs.environs import env


FERNET_KEY = env.str("FERNET_KEY")
f = fernet.Fernet(FERNET_KEY)


async def get_count(db, q, model):
    """
    Get the count of records matching the query.

    Args:
        db: The database session.
        q: The query object to count the results of.
        model: The SQLAlchemy model for the query.

    Returns:
        int: The count of matching records.
    """
    count_query = q.with_only_columns(func.count(model.id))
    count = await db.execute(count_query)
    return count.scalar_one()


async def encode_id(identifier: int) -> str:
    """
    Encode an integer identifier into a secure string using Fernet encryption.

    Args:
        identifier (int): The identifier to encode.

    Returns:
        str: The encoded identifier as a string.
    """
    encoded_identifier = f.encrypt(str(identifier).encode())
    return encoded_identifier.decode()


async def decode_id(token: str) -> int:
    """
    Decode a previously encoded identifier string back to its integer form.

    Args:
        token (str): The encoded identifier string to decode.

    Returns:
        int: The decoded identifier as an integer.
    """
    encoded_identifier = f.decrypt(token.encode())
    return int(encoded_identifier.decode())
