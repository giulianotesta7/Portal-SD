import smtplib
import os
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))

def enviar_mail_entrega(usuario, tecnico, pdf_path):
    remitente = "entrega-activos@emergencias.com.ar"  
    destinatario = f"{usuario}@emergencias.com.ar"
    copia = f"{tecnico}@emergencias.com.ar"

    asunto = f"Solicitud de entrega - {usuario.upper()}"
    cuerpo = (
        f'En el siguiente correo se adjunta la solicitud de entrega del usuario "{usuario.upper()}".\n\n'
        "Si aún no recibió el equipo, ya se van a comunicar para pasar a retirarlo y firmar el comprobante en el lugar."
    )

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Cc"] = copia
    msg.set_content(cuerpo)

    
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            tipo_mime, _ = mimetypes.guess_type(pdf_path)
            if tipo_mime:
                tipo, subtipo = tipo_mime.split('/')
            else:
                tipo, subtipo = "application", "octet-stream"
            msg.add_attachment(f.read(), maintype=tipo, subtype=subtipo, filename=os.path.basename(pdf_path))
    else:
        raise FileNotFoundError(f"No se encontró el archivo PDF: {pdf_path}")

    
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:  
            smtp.send_message(msg)
    except Exception as e:
            print(f"Error al enviar correo: {e}")


