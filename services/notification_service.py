from models.notifications import Notification


def create_notification(db, user_id: int, title: str, message: str):
    notification = Notification(user_id=user_id, title=title, message=message)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_user_notifications(db, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).all()