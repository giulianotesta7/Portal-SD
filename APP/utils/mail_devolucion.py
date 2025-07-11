import smtplib
import os
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))

def enviar_mail_devolucion(usuario, tecnico, jefe, pdf_path,nombre_completo):
    remitente = "devolucion-activos@empresa.com.ar"
    destinatario = usuario
    copias = [tecnico, jefe]

    asunto = f"Comprobante de Devolución - {nombre_completo}"
    cuerpo = (
        f'Se adjunta el comprobante de devolución del usuario {nombre_completo}.\n\n'
        "Saludos."
    )

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Cc"] = ", ".join(copias)

    msg.set_content(cuerpo)

    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            tipo_mime, _ = mimetypes.guess_type(pdf_path)
            tipo, subtipo = tipo_mime.split("/") if tipo_mime else ("application", "octet-stream")
            msg.add_attachment(f.read(), maintype=tipo, subtype=subtipo, filename=os.path.basename(pdf_path))
    else:
        raise FileNotFoundError(f"No se encontró el archivo PDF: {pdf_path}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.send_message(msg)
    except Exception as e:
        print(f"Error al enviar correo: {e}")

