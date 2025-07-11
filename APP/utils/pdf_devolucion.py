from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os
from reportlab.lib.utils import ImageReader
from PIL import Image
from io import BytesIO
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import black

def draw_wrapped_text(canvas, text, x, y, max_width, leading=20):
    lines = []
    current_line = ''
    for word in text.split():
        test_line = f"{current_line} {word}".strip()
        if stringWidth(test_line, "Helvetica", 12) <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    for line in lines:
        canvas.drawString(x, y, line)
        y -= leading

    return y

def generar_pdf_devolucion(
    nombre,
    legajo,
    tipo,
    marca,
    nro_etiqueta,
    otros_articulos,
    aclaracion_empleado,
    aclaracion_receptor,
    firma_empleado_path,
    firma_receptor_path,
    fecha,
    id_form,
    rol_receptor,
    logo_path=None
):
    
    if isinstance(fecha, str):
        fecha = datetime.strptime(fecha, "%Y-%m-%d")

    # Crear carpeta 
    año, mes, dia = fecha.strftime("%Y"), fecha.strftime("%m"), fecha.strftime("%d")
    carpeta_destino = os.path.join("pdfs","pdfs_devolucion", año, mes, dia)
    os.makedirs(carpeta_destino, exist_ok=True)

    # Ruta final
    pdf_filename = f"{id_form}_{nombre.replace(' ', '_')}.pdf"
    pdf_path = os.path.join(carpeta_destino, pdf_filename)

    # Crear canvas
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y = height - 50
    lh = 20
    max_width = 500

    #LOGO
    if logo_path and os.path.exists(logo_path):
        logo_width, logo_height = 80, 40
        c.drawImage(logo_path, width - 90, y - logo_height + 40, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, "CONSTANCIA DE DEVOLUCIÓN DE EQUIPAMIENTO")
    y -= 14
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y, "INTERNATIONAL HEALTH SERVICES ARGENTINA S.A.")
    y -= 14

    # Línea negra horizontal
    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.line(40, y, width - 40, y)
    y -= lh

    # Fecha
    c.setFont("Helvetica", 12)
    c.drawRightString(width - 50, y, f"Buenos Aires, {fecha.strftime('%d/%m/%Y')}")
    y -= lh * 2

    # Texto 
    texto_principal = (
        f"{nombre}, Legajo N° {legajo or '____'}, dejo constancia que el día de la fecha "
        f"realicé devolución a la empresa INTERNATIONAL HEALTH SERVICES ARGENTINA S.A. de una {tipo.upper()}, MARCA: {marca.upper()}, "
        f"CON N° INTERNO DE MÁQUINA {nro_etiqueta or '____'} JUNTO CON SU CARGADOR."
    )
    y = draw_wrapped_text(c, texto_principal, 50, y, max_width)

    # Artículos adicionales
    if otros_articulos:
        y = draw_wrapped_text(c, f"Así como de los siguientes artículos: {otros_articulos}.", 50, y, max_width)

    # Cierre
    y = draw_wrapped_text(c, "Con motivo de la finalización del vínculo laboral que nos unía.", 50, y, max_width)
    y -= lh * 2

    # Firma del empleado
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "FIRMA DEL EMPLEADO:")
    y -= (lh + 5)

    if os.path.exists(firma_empleado_path):
        firma_width, firma_height = 220, 70
        image = Image.open(firma_empleado_path).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        firma_image = ImageReader(buffer)
        c.drawImage(firma_image, 50, y - firma_height, width=firma_width, height=firma_height, mask='auto')
    y -= 90

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"ACLARACIÓN: {aclaracion_empleado or ''}")
    y -= lh * 2

    # Firma del receptor
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, f"FIRMA DEL {rol_receptor.upper()}:")
    y -= (lh + 5)

    if os.path.exists(firma_receptor_path):
        firma_width, firma_height = 220, 70
        image = Image.open(firma_receptor_path).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        firma_image = ImageReader(buffer)
        c.drawImage(firma_image, 50, y - firma_height, width=firma_width, height=firma_height, mask='auto')
    y -= 90

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"ACLARACIÓN: {aclaracion_receptor or ''}")

    c.save()
    return pdf_path
