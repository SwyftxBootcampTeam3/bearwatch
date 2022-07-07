from typing import List
from fastapi import APIRouter, Depends, Body, status, HTTPException


# dependencies
from app.api.dependencies.database import get_repository
from app.api.dependencies.auth import get_current_user

# models
from app.models.alert import Alert, AlertCreate, AlertUpdate

# repositories
from app.db.repositories.alerts import AlertsRepository

# services
from app.models.user import User

from app.services.celery_worker import update_assets, get_triggered_alerts

router = APIRouter()


@router.get("/", response_model=List[Alert], name="alerts:get-user-alerts")
async def get_user_alerts(
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> List[Alert]:
    ''' 
    Get a users alerts
    '''

    user_alerts = await alerts_repo.get_alerts_by_user_id(current_user.id)
    return user_alerts


@router.post("/", response_model=Alert, name="alerts:create-alert")
async def create_alert(
    request: AlertCreate = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> Alert:
    ''' 
    Create an alert
    '''

    #Ensure the authenticated user is the one making the request
    if current_user.id != request.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only create an alert for yourself!",
        )

    alert = await alerts_repo.create_alert(new_alert=request)
    return alert


@router.put("/", name="alerts:update-alert")
async def update_alert(
    alert_id: int,
    request: AlertUpdate = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> Alert:
    '''
    Update an alerts price/type
    '''

    # Get the alert to check the user owns the alert
    alert = await alerts_repo.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That alert does not exist!",
        )
    if current_user.id != alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    # Update the alert and return the updated alert
    await alerts_repo.update_alert(alert_id=alert_id, updated_alert=request)
    return await alerts_repo.get_alert_by_id(id=alert_id)

@router.put("/sleep", name="alerts:sleep-alert")
async def sleep_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> None:
    '''
    Sleep an alert (Active = False)
    '''

    # Get the alert to check the user owns the alert
    alert = await alerts_repo.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That alert does not exist!",
        )

    if current_user.id != alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    await alerts_repo.sleep_alert_by_id(alert_id=alert_id)

@router.put("/unsleep", name="alerts:unsleep-alert")
async def unsleep_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> None:
    '''
    Unsleep an alert (Active = True)
    '''

    # Get the alert to check the user owns the alert
    alert = await alerts_repo.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That alert does not exist!",
        )

    if current_user.id != alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    await alerts_repo.unsleep_alert_by_id(alert_id=alert_id)


@router.delete("/", name="alerts:delete-alert")
async def delete_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    alerts_repo: AlertsRepository = Depends(get_repository(AlertsRepository))
) -> None:
    '''
    Soft delete an alert
    '''

    # Get the alert to check the user owns the alert
    alert = await alerts_repo.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That alert doees not exist!",
        )

    if current_user.id != alert.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only update an alert for yourself!",
        )

    await alerts_repo.delete_alert_by_id(alert_id=alert_id)


@router.post("/trigger", name="assets:get-all-assets")
async def trigger_alerts() -> None:
    '''
    Get all assets in the db given an authenticated request
    '''
    await get_triggered_alerts()