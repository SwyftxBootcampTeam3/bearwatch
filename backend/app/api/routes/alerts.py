from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm  # JWT


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.token import AccessToken
from app.models.alert import Alert, AlertCreate, AlertUpdate, AlertDelete

# repositories
from app.db.repositories.alerts import AlertsRepository

# services
from app.services.authentication import AuthService
from app.models.user import User

router = APIRouter()


# name the route and you can use it across testing and db access
@router.get("/", response_model=List[Alert], name="alerts:get-user-alerts")
async def get_user_alerts(
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> List[Alert]:

    user_alerts = await alerts_repo.get_alerts_by_user_id(current_user.id)
    return user_alerts


@router.post("/", response_model=Alert, name="alerts:create-alert")
async def create_alert(
    new_alert: AlertCreate = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> Alert:

    new_alert.user_id = current_user.id
    alert = await alerts_repo.create_alert(new_alert=new_alert)
    return alert


@router.put("/", name="alerts:update-alert")
async def update_alert(
    updated_alert: AlertUpdate = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> Alert:

    if current_user.id != updated_alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    await alerts_repo.update_alert(updated_alert=updated_alert)
    alert = await alerts_repo.get_alert_by_id(id=updated_alert.id)
    return alert


@router.delete("/", name="alerts:delete-alert")
async def update_alert(
    deleted_alert: AlertDelete = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> None:
    if current_user.id != deleted_alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    await alerts_repo.delete_alert(deleted_alert=deleted_alert)
