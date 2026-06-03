from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies.auth import get_current_user
from schemas.notifications import NotificationResponse
from services.notification_service import get_user_notifications

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=list[NotificationResponse])
def my_notifications(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_notifications(db, current_user.id)