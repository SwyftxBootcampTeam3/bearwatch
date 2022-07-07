from typing import List
from fastapi import APIRouter, Depends


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.asset import Asset

# repositories
from app.db.repositories.assets import AssetsRepository

# services
from app.services.celery_worker import update_assets, get_triggered_alerts
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[Asset], name="assets:get-all-assets")
async def get_all_assets(
    current_user: User = Depends(get_current_user),
    assets_repo: AssetsRepository = Depends(get_repository(AssetsRepository))
) -> List[Asset]:
    '''
    Get all assets in the db given an authenticated request
    '''

    assets = await assets_repo.get_all_assets()
    return assets


@router.get("/test", name="assets:get-all-assets")
async def get_all_assets() -> None:
    '''
    Get all assets in the db given an authenticated request
    '''
    await get_triggered_alerts()
    print('Done')