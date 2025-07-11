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

load_dotenv()
LOGO_PATH = os.getenv("LOGO_PATH")

@router.get("/formulario_devolucion", response_class=HTMLResponse,)
async def get_devolucion(request: Request,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("formulario_devolucion.html", {"request": request, "user": user})

@router.post("/formulario_devolucion", response_class=HTMLResponse)
async def post_devolucion(
    request: Request,
    fecha: str = Form(...),
    nombre: str = Form(...),
    legajo: str = Form(...),
    tipo: str = Form(...),
    marca: str = Form(...),
    nro_etiqueta: str = Form(...),
    otros_articulos: str = Form(...),
    aclaracion_empleado: str = Form(...),
    aclaracion_receptor: str = Form(...),
    firma_empleado: str = Form(...),
    firma_receptor: str = Form(...),
    rol_receptor: str = Form(...),
    mail_usuario: str = Form(...),
    mail_tecnico: str = Form(...),
    mail_jefe: str = Form(...),
    db: Session = Depends(get_db)
):
    def guardar_firma(base64_data, filename):
        _, encoded = base64_data.split(",", 1) if "," in base64_data else ("", base64_data)
        firma_bytes = base64.b64decode(encoded)
        firma_image = Image.open(BytesIO(firma_bytes))

        if firma_image.mode in ("RGBA", "LA"):
            fondo = Image.new("RGB", firma_image.size, (255, 255, 255))
            fondo.paste(firma_image, mask=firma_image.split()[3])
            firma_image = fondo
        else:
            firma_image = firma_image.convert("RGB")

        os.makedirs("firmas", exist_ok=True)
        path = os.path.join("firmas", filename)
        firma_image.save(path, format="PNG")
        return path

    firma_empleado_path = guardar_firma(firma_empleado, f"{nombre.replace(' ', '_')}_empleado.png")
    firma_receptor_path = guardar_firma(firma_receptor, f"{nombre.replace(' ', '_')}_receptor.png")

    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
    nuevo_form = formulario_de_devolucion(
        fecha=fecha_obj,
        nombre=nombre,
        legajo=legajo,
        marca=marca,
        nro_etiqueta=nro_etiqueta,
        otros_articulos=otros_articulos,
        aclaracion_empleado=aclaracion_empleado,
        aclaracion_receptor=aclaracion_receptor
    )
    db.add(nuevo_form)
    db.commit()
    db.refresh(nuevo_form)

    pdf_path = generar_pdf_devolucion(
        id_form=nuevo_form.id,
        fecha=fecha,
        nombre=nombre,
        legajo=legajo,
        tipo=tipo,
        marca=marca,
        nro_etiqueta=nro_etiqueta,
        otros_articulos=otros_articulos,
        rol_receptor=rol_receptor,
        aclaracion_empleado=aclaracion_empleado,
        aclaracion_receptor=aclaracion_receptor,
        firma_empleado_path=firma_empleado_path,
        firma_receptor_path=firma_receptor_path,
        logo_path=LOGO_PATH
    )

    mensaje_mail_enviado = True
    try:
        enviar_mail_devolucion(mail_usuario, mail_tecnico, mail_jefe, pdf_path, nombre)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        mensaje_mail_enviado = False

    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("formulario_devolucion.html", {
        "request": request,
        "mensaje_exito": True,
        "mensaje_mail_enviado": mensaje_mail_enviado,
        "fecha_actual": datetime.now().strftime("%Y-%m-%d"),
        "user": user,
    })