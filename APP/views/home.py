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

templates = Jinja2Templates(directory="APP/template")
router = APIRouter(dependencies=[Depends(require_login)]) 

@router.get("/", response_class=HTMLResponse)
@restrict_users(["user_RRHH"])
async def get_home(request: Request, db: Session = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("home.html", {"request": request, "user": user})