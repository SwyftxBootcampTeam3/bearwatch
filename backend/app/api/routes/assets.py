from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # JWT


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.token import AccessToken
from app.models.asset import Asset

# repositories
from app.db.repositories.assets import AssetsRepository

# services
from app.services.authentication import AuthService
from app.models.user import User

router = APIRouter()


# name the route and you can use it across testing and db access
@router.get("/", response_model=List[Asset], name="assets:get-all-assets")
async def get_all_assets(
    current_user: User = Depends(get_current_user),
    assets_repo: AssetsRepository = Depends(get_repository(AssetsRepository))
) -> List[Asset]:

    assets = await assets_repo.get_all_assets()
    return assets