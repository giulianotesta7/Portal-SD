from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from io import BytesIO
import base64
from PIL import Image
import os
from APP.utils.pdf_entrega import generar_pdf_entrega
from APP.utils.pdf_devolucion import generar_pdf_devolucion
from datetime import datetime, date
from sqlalchemy.orm import Session
from APP.models import dispositivo, formulario_de_entrega, formulario_de_devolucion, consumible, stock_leasing
from APP.models import user as User
from APP.db import get_db
from typing import Optional
from starlette.status import HTTP_303_SEE_OTHER
from dotenv import load_dotenv
from APP.utils.mail_entrega import enviar_mail_entrega
from APP.utils.require_login import require_login
from APP.utils.mail_devolucion import enviar_mail_devolucion
from APP.utils.role_restriction import restrict_users

router = APIRouter(dependencies=[Depends(require_login)]) 
templates = Jinja2Templates(directory="APP/template")

@router.get("/stock_1", response_class=HTMLResponse)
@restrict_users(["user_RRHH"])
async def get_stock_1(request: Request, db: Session = Depends(get_db)):
    dispositivos = db.query(dispositivo).filter(dispositivo.organismo == "stock_1").order_by(dispositivo.nombre.asc()).all()
    consumibles = db.query(consumible).filter(consumible.organismo == "stock_1").order_by(consumible.nombre.asc()).all()
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("stock_1.html", {
        "request": request,
        "dispositivos": dispositivos,
        "consumibles": consumibles,
        "user": user
    })


@router.post("/stock_1/update_consumible")
@restrict_users(["user_RRHH"])
async def update_consumible(
    request: Request,
    consumible_id: int = Form(...),
    action: str = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    consumible_item = db.query(consumible).filter(consumible.id == consumible_id).first()
    if consumible_item:
        if action == "increment":
            consumible_item.cantidad += cantidad
        elif action == "decrement":
            consumible_item.cantidad = max(0, consumible_item.cantidad - cantidad)
        db.commit()
    return RedirectResponse(url="/stock_1", status_code=303)


@router.post("/stock_1/update_dispositivo")
@restrict_users(["user_RRHH"])
async def update_dispositivo(
    request: Request,
    dispositivo_id: int = Form(...),
    action: str = Form(...),
    cantidad: int = Form(...),
    db: Session = Depends(get_db)
):
    dispositivo_item = db.query(dispositivo).filter(dispositivo.id == dispositivo_id).first()
    if dispositivo_item:
        if action == "increment":
            dispositivo_item.cantidad += cantidad
        elif action == "decrement":
            dispositivo_item.cantidad = max(0, dispositivo_item.cantidad - cantidad)
        db.commit()
    return RedirectResponse(url="/stock_1", status_code=303)