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


@router.get("/formulario_entrega", response_class=HTMLResponse)
@restrict_users(["user_RRHH"])
async def get_entrega(request: Request, db: Session = Depends(get_db)):
    dispositivos = db.query(dispositivo).all()
    accesorios = db.query(dispositivo).filter(dispositivo.accesorio == True).all()
    fecha_actual = date.today().strftime("%Y-%m-%d")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("formulario_entrega.html", {
        "request": request,
        "dispositivos": dispositivos,
        "accesorios": accesorios,
        "fecha_actual": fecha_actual,
        "user": user
    })

@router.post("/formulario_entrega", response_class=HTMLResponse)
@restrict_users(["user_RRHH"])
async def post_entrega(
    request: Request,
    dispositivo_id: int = Form(...),
    modelo: str = Form(None),
    cant_dispositivo: int = Form(...),
    etiqueta: str = Form(...),
    accesorio1: Optional[str] = Form(None),
    cant_accesorio1: Optional[str] = Form(None),
    accesorio2: Optional[str] = Form(None),
    cant_accesorio2: Optional[str] = Form(None),
    accesorio3: Optional[str] = Form(None),
    cant_accesorio3: Optional[str] = Form(None),
    organismo: str = Form(...),
    usuario: str = Form(...),
    nroTicket: str = Form(None),
    tecnico: str = Form(...),
    fecha: str = Form(...),
    observaciones: str = Form(None),
    leasing: str = Form(None),
    firma: str = Form(...),
    db: Session = Depends(get_db)
):
    def parse_cantidad(valor):   
        try:
            return int(valor) if valor else None
        except ValueError:
            return None

    cant1 = parse_cantidad(cant_accesorio1)
    cant2 = parse_cantidad(cant_accesorio2)
    cant3 = parse_cantidad(cant_accesorio3)
    es_leasing = leasing is not None
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")

    #Guardar firma 
    _, encoded = firma.split(",", 1) if "," in firma else ("", firma)
    firma_bytes = base64.b64decode(encoded)
    image = Image.open(BytesIO(firma_bytes))
    os.makedirs("firmas", exist_ok=True)
    firma_temp_path = os.path.join("firmas", "firma_temp.png")
    image.save(firma_temp_path)

    # Nombre dispositivo
    dispositivo_obj = db.query(dispositivo).filter(
        dispositivo.id == dispositivo_id,
        dispositivo.organismo == organismo
    ).first()
    nombre_dispositivo = dispositivo_obj.nombre if dispositivo_obj else "Desconocido"

    #Crear el form
    nuevo_formulario = formulario_de_entrega(
        dispositivo_id=dispositivo_id,
        modelo=modelo,
        etiqueta=etiqueta,
        cant_dispositivo=cant_dispositivo,
        accesorio1=accesorio1,
        cant_accesorio1=cant1,
        accesorio2=accesorio2,
        cant_accesorio2=cant2,
        accesorio3=accesorio3,
        cant_accesorio3=cant3,
        organismo=organismo,
        usuario=usuario,
        nroTicket=nroTicket,
        tecnico=tecnico,
        fecha=fecha_obj,
        observaciones=observaciones,
        leasing=es_leasing
    )
    db.add(nuevo_formulario)

    if es_leasing:
        stock = db.query(stock_leasing).first()
        stock.cantidad -= 1

    db.commit()
    db.refresh(nuevo_formulario)

    # Renombra firma con ID 
    firma_filename = f"{nuevo_formulario.id}-{usuario.replace(' ', '_').upper()}_firma.png"
    firma_path = os.path.join("firmas", firma_filename)
    os.rename(firma_temp_path, firma_path)

    # Descuenta stock
    if dispositivo_obj and dispositivo_obj.cantidad >= cant_dispositivo:
        dispositivo_obj.cantidad -= cant_dispositivo
    else:
        print("⚠️ No hay suficiente stock del dispositivo principal.")

    # Descuenta stock accesorios
    for accesorio_nombre, cantidad in [
        (accesorio1, cant1),
        (accesorio2, cant2),
        (accesorio3, cant3)
    ]:
        if accesorio_nombre and cantidad:
            accesorio_obj = db.query(dispositivo).filter(
                dispositivo.nombre == accesorio_nombre,
                dispositivo.accesorio == True,
                dispositivo.organismo == organismo
            ).first()
            if accesorio_obj and accesorio_obj.cantidad >= cantidad:
                accesorio_obj.cantidad -= cantidad
            else:
                print(f"⚠️ No hay suficiente stock del accesorio: {accesorio_nombre}")

    db.commit()

    # Crea carpeta
    actual = datetime.now()
    año, mes, dia = str(actual.year), f"{actual.month:02d}", f"{actual.day:02d}"
    carpeta_destino = os.path.join("pdfs","pdfs_entrega", año, mes, dia)
    os.makedirs(carpeta_destino, exist_ok=True)
    pdf_filename = f"{nuevo_formulario.id}-{usuario.replace(' ', '_').upper()}-ENTREGA-DE-EQUIPAMIENTO.pdf"
    pdf_path = os.path.join(carpeta_destino, pdf_filename)

    # Genera PDF
    generar_pdf_entrega(
        usuario, firma_path, pdf_path,
        nombre_dispositivo, organismo, nroTicket,
        tecnico, observaciones, fecha_obj.strftime("%d/%m/%Y"),
        cant_dispositivo=cant_dispositivo,
        accesorio1=accesorio1, cant_accesorio1=cant1,
        accesorio2=accesorio2, cant_accesorio2=cant2,
        accesorio3=accesorio3, cant_accesorio3=cant3,
        etiqueta=etiqueta,
        modelo=modelo,
        logo_path=LOGO_PATH,
    )

    
    try:
        enviar_mail_entrega(usuario, tecnico, pdf_path)
    except Exception as e:
        print(f"⚠️ No se pudo enviar el correo: {e}")

    
    dispositivos = db.query(dispositivo).all()
    fecha_actual = date.today().strftime("%Y-%m-%d")
    user = db.query(User).filter(User.id == request.session["user_id"]).first()
    return templates.TemplateResponse("formulario_entrega.html", {
        "request": request,
        "firma_guardada": True,
        "firma_path": firma_path,
        "pdf_path": pdf_path,
        "dispositivos": dispositivos,
        "fecha_actual": fecha_actual,
        "user": user,
    })