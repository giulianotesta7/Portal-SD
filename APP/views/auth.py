from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from starlette.status import HTTP_303_SEE_OTHER
from passlib.hash import pbkdf2_sha256
from APP.models import user as user_model
from APP.db import get_db  
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="APP/template")


@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_post(request: Request, user: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    usuario = db.query(user_model).filter_by(user=user).first()
    if usuario and pbkdf2_sha256.verify(password, usuario.password):
        request.session["user_id"] = usuario.id
        return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request, "error": "Credenciales inválidas"})


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
