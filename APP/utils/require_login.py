from fastapi import Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

def require_login(request: Request):
    if "user_id" not in request.session:
        raise HTTPException(status_code=HTTP_303_SEE_OTHER, headers={"Location": "/login"})
    return True
