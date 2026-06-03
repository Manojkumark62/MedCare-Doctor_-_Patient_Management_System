from enum import Enum
from fastapi import Depends, HTTPException
from dependencies.auth import get_current_user


def _normalize_role(role):
    if isinstance(role, Enum):
        return role.value.lower()
    return str(role).lower()


def role_required(roles: list):
    normalized_roles = {_normalize_role(role) for role in roles}

    def verify_role(current_user = Depends(get_current_user)):
        current_role = _normalize_role(current_user.role)
        if current_role not in normalized_roles:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return current_user
    return verify_role