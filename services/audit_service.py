from models.audit_logs import AuditLog

def create_audit_log(db, user_id: int, action: str, entity: str):
    log = AuditLog(user_id=user_id, action=action, entity=entity)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log