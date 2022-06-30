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

GET_USER_BY_EMAIL_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at
    FROM users
    WHERE email = :email;
"""

GET_USER_BY_PHONE_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at
    FROM users
    WHERE phone_number = :phone_number;
"""

GET_USER_BY_EMAIL_AND_PHONE_QUERY = """
    SELECT id, email, phone_number, created_at, updated_at
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

        if user:
            user = User(**user)

        return user

    async def get_user_by_phone_number(self, *, phone_number: int) -> User:
        """
        Queries the database for the first matching user with this phone number.
        """

        # pass values to query
        user = await self.db.fetch_one(
            query=GET_USER_BY_PHONE_QUERY, values={
                "phone_number": phone_number}
        )

        if user:
            user = User(**user)

        return user

    async def get_user_by_email_and_phone(self, *, email: EmailStr, phone_number: int) -> User:
        """
        Queries the database for the first matching user with this email & phone
        """

        # pass values to query
        user = await self.db.fetch_one(
            query=GET_USER_BY_EMAIL_AND_PHONE_QUERY, values={
                "email": email, "phone_number": phone_number}
        )

        if user:
            user = User(**user)

        return user

    async def check_user_already_exists(self, *, email: EmailStr, phone_number: int) -> int:
        '''
        Queries the database to check the email or phone number provided is already in use
        '''

        user_with_email = await self.get_user_by_email(email=email)
        if user_with_email is not None:
            return 1
        user_with_phone = await self.get_user_by_phone_number(phone_number=phone_number)
        if user_with_phone is not None:
            return 2
        return 0

    async def create_user(self, *, new_user: UserCreate) -> User:
        """
        Creates a user.
        """

        # unique constraints exist on email & phome -> confirm both are not taken
        user_exists = await self.check_user_already_exists(email=new_user.email, phone_number=new_user.phone_number)

        if user_exists == 0:  # User doesnt exist
            # create user in database
            created_user = await self.db.fetch_one(
                query=CREATE_USER_QUERY, values={
                    "email": new_user.email, "phone_number": new_user.phone_number}
            )
            return User(**created_user)
        elif user_exists == 1:  # Email is in use
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That email is already in use! Login or try another.",
            )
        elif user_exists == 2:  # Phone is in use
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="That phone number is already in use! Login or try another.",
            )
        else:  # Unknown Error
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown error. Please try again later",
            )

    async def authenticate_user(
        self, *, email: EmailStr
    ) -> Optional[User]:
        """
        Authenticate supplied email with a user in database. Return None if none exists
        """

        # check for existence using email
        user_in_db = await self.get_user_by_email(email=email)

        if not user_in_db:
            return None

        return user_in_db
