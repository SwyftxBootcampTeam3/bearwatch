
from fastapi import APIRouter
from app.api.routes.users import router as users_router
from app.api.routes.assets import router as assets_router
from app.api.routes.alerts import router as alerts_router

router = APIRouter()

router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(assets_router, prefix="/assets", tags=["assets"])
router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
