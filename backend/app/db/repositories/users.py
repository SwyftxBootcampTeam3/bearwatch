from typing import Optional
from databases import Database

# app
from pydantic import EmailStr
from fastapi import HTTPException, status

# repositories
from app.db.repositories.base import BaseRepository

# from app.db.repositoris.profiles import ProfilesRepository

# models
from app.models.user import UserCreate, UserUpdate, User

CREATE_USER_QUERY = """
    INSERT INTO users (email,phone_number)
    VALUES (:email,:phone_number)
    RETURNING id, email, phone_number, created_at, updated_at;
"""

# don't use select *. bad.
GET_USER_BY_EMAIL_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at;
    FROM users
    WHERE email = :email;
"""

GET_USER_BY_PHONE_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at;
    FROM users
    WHERE phone_number = :phone_number;
"""

GET_USER_BY_EMAIL_AND_PHONE_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at;
    FROM users
    WHERE email = :email AND phone_number = :phone_number;
"""


class UsersRepository(BaseRepository):
    """
    All database actions associated with Users
    """

    # when we init we want to ensure that the auth service is available to the repository --> we're going to be doing auth things
    def __init__(self, db: Database) -> None:
        """
        Standard repository intialise + auth_service + profiles_repo available
        """
        super().__init__(db)


    async def get_user_by_email(self, *, email: EmailStr) -> User:
        """
        Queries the database for the first matching user with this email.
        """

        # pass values to query
        user = await self.db.fetch_one(
            query=GET_USER_BY_EMAIL_QUERY, values={"email": email}
        )

        # if user, return UserInDB else None
        if user:
            user = User(**user)

            # perform any other modifications on returning inDB model here TODO
            # e.g. masking password/hash/private details
        return user

    async def get_user_by_email_and_phone(self, *, email: EmailStr, phone_number:str) -> User:
        """
        Queries the database for the first matching user with this email & phone
        """

        # pass values to query
        user = await self.db.fetch_one(
            query=GET_USER_BY_EMAIL_AND_PHONE_QUERY, values={"email": email, "phone_number": phone_number}
        )

        # if user, return UserInDB else None
        if user:
            user = User(**user)

            # perform any other modifications on returning inDB model here TODO
            # e.g. masking password/hash/private details
        return user

    async def create_user(self, *, new_user: UserCreate) -> User:
        """
        Creates a user.
        """

        # unique constraints exist on email -> confirm is not taken
        existing_user = await self.get_user_by_email_and_phone(email=new_user.email, phone_number=new_user.phone_number)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is alredy taken. Login or try another.",
            )

        # create user in database
        created_user = await self.db.fetch_one(
            query=CREATE_USER_QUERY, values={"email":new_user.email, "phone_number":new_user.phone_number}
        )

        return created_user

    async def authenticate_user(
        self, *, email: EmailStr
    ) -> Optional[User]:
        """
        Authenticate supplied email + phone matches a user in database. Return None if not valid/DNE.
        """

        # check for existence using email
        user_in_db = await self.get_user_by_email(email=email)

        if not user_in_db:
            return None

        return user_in_db