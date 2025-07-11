from functools import wraps
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_303_SEE_OTHER
from APP.models import user as User

def restrict_users(denied_users: list[str], redirect_to: str = "/glpi"):
    def decorator(view_func):
        @wraps(view_func)
        async def wrapper(*args, **kwargs):
            
            request: Request = kwargs.get("request") or args[0]
            db: Session = kwargs.get("db")

            if not db:
                for arg in args:
                    if isinstance(arg, Session):
                        db = arg
                        break

            user = db.query(User).filter(User.id == request.session["user_id"]).first()
            if user.user in denied_users:
                return RedirectResponse(url=redirect_to, status_code=HTTP_303_SEE_OTHER)

            return await view_func(*args, **kwargs)
        return wrapper
    return decorator
