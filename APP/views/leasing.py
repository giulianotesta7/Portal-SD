from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from APP.models import formulario_de_entrega, stock_leasing
from APP.models import user as User
from APP.db import get_db
from starlette.status import HTTP_303_SEE_OTHER
from APP.utils.role_restriction import restrict_users
from APP.utils.require_login import require_login

router = APIRouter(dependencies=[Depends(require_login)]) 
templates = Jinja2Templates(directory="APP/template")

@router.get("/leasing", response_class=HTMLResponse)
@restrict_users(["user_RRHH"])
async def get_entrega(request: Request, db: Session = Depends(get_db)):
    dispositivos = db.query(formulario_de_entrega).filter(formulario_de_entrega.leasing == True).order_by(formulario_de_entrega.id.desc()).all()
    cantidad = db.query(stock_leasing.cantidad).scalar()
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("leasing.html", {
        "request": request,
        "dispositivos": dispositivos,
        "cantidad": cantidad,
        "user": user

    })

@router.post("/marcar_devuelto/{formulario_id}")
@restrict_users(["user_RRHH"])
async def marcar_como_devuelto(request: Request,formulario_id: int, db: Session = Depends(get_db)):
    form = db.query(formulario_de_entrega).filter_by(id=formulario_id).first()
    if form:
        form.devuelto = True
        stock = db.query(stock_leasing).first()
        stock.cantidad += 1
        db.commit()
    return RedirectResponse(url="/leasing", status_code=HTTP_303_SEE_OTHER)

