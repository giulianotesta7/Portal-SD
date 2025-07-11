from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os

class SignatureLine(Flowable):
    def __init__(self, width=200, label="Firma"):
        Flowable.__init__(self)
        self.width = width
        self.label = label

    def draw(self):
        self.canv.line(0, 0, self.width, 0)
        self.canv.setFont("Helvetica", 8)
        self.canv.drawCentredString(self.width / 2, -10, self.label)

def generar_pdf_entrega(
    usuario, firma_path, output_path,
    dispositivo, organismo, nroTicket,
    tecnico, observaciones, fecha,
    cant_dispositivo=1,
    accesorio1=None, cant_accesorio1=None,
    accesorio2=None, cant_accesorio2=None,
    accesorio3=None, cant_accesorio3=None,
    etiqueta=None,
    modelo=None,
    leasing=False,
    id_form=None,
    logo_path=None
):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    elements = []

    title_style = styles['Title']
    normal_style = styles['Normal']
    bold_style = ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold')

    if logo_path and os.path.exists(logo_path):
        logo = Image(logo_path, width=80, height=40)
        logo.hAlign = 'RIGHT'
        elements.append(logo)

    # Título
    elements.append(Paragraph("ENTREGA DE EQUIPAMIENTO", title_style))
    elements.append(Paragraph(" ", styles['Italic']))
    elements.append(Spacer(1, 12))



    # Sección: Información del receptor y del equipo
    data_info = [
        [
            Paragraph("<b>INFORMACIÓN</b>", bold_style),
            Paragraph("<b>EQUIPAMIENTO </b>", bold_style)
        ],
        [
            Paragraph(f"Usuario: {usuario}<br/>Técnico Responsable: {tecnico}", normal_style),
            Paragraph(f"Dispositivo: {dispositivo} (x{cant_dispositivo})<br/>Modelo: {modelo or '-'}<br/>Etiqueta: {etiqueta or '-'}", normal_style)
        ]
    ]

    table_info = Table(data_info, colWidths=[270, 250])
    table_info.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 1), (-1, 1), 0.25, colors.gray),
        ('LEFTPADDING', (0, 1), (-1, 1), 6),
        ('RIGHTPADDING', (0, 1), (-1, 1), 6)
    ]))
    elements.append(table_info)
    elements.append(Spacer(1, 12))

    # Sección: Datos administrativos y accesorios
    accesorios = []
    for nombre, cantidad in [
        (accesorio1, cant_accesorio1),
        (accesorio2, cant_accesorio2),
        (accesorio3, cant_accesorio3)
    ]:
        if nombre and nombre.strip():
            texto = nombre.strip()
            if cantidad and int(cantidad) > 0:
                texto += f" (x{cantidad})"
            accesorios.append(texto)
    accesorios_str = "<br/>".join(accesorios) if accesorios else "-"

    data_admin = [
        [
            Paragraph("<b>DATOS </b>", bold_style),
            Paragraph("<b>ACCESORIOS </b>", bold_style)
        ],
        [
            Paragraph(f"Organismo: {organismo}<br/>N° de Ticket: {nroTicket or '-'}<br/>Fecha de Entrega: {fecha}", normal_style),
            Paragraph(accesorios_str, normal_style)
        ]
    ]

    table_admin = Table(data_admin, colWidths=[270, 250])
    table_admin.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 0.25, colors.gray),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 1), (-1, 1), 6),
        ('RIGHTPADDING', (0, 1), (-1, 1), 6)
    ]))
    elements.append(table_admin)
    elements.append(Spacer(1, 12))

    # Sección: Observaciones
    elements.append(Paragraph("<b>OBSERVACIONES</b>", bold_style))
    elements.append(Paragraph(observaciones or "Sin observaciones.", normal_style))
    elements.append(Spacer(1, 20))

    # Firma escaneada 
    if os.path.exists(firma_path):
        elements.append(Paragraph("Firma:", bold_style))
        elements.append(Spacer(1, 6))
        firma = Image(firma_path, width=150, height=50)
        firma.hAlign = 'LEFT'
        elements.append(firma)

    # Pie de página
    footer_text = (
    "<b>IMPORTANTE:</b> Los elementos entregados son para uso exclusivo como herramienta de trabajo "
    "para el desempeño de mis actividades (no se permite colocar ningún tipo de decoración sobre el equipo), "
    "con ocasión del vínculo laboral que nos une, quedando excluido su uso para fines personales.<br/><br/>"
    "Asimismo, dejo constancia que me comprometo a su inmediata devolución, en las mismas condiciones en que "
    "se me fuera entregada en la oportunidad de extinción de la relación laboral, por cualquier causa o requerimiento de la empresa.<br/><br/>"
    "En caso de no devolver los dispositivos que se entregaron como herramienta de trabajo, te haremos saber que "
    "podremos retener el importe por el valor equivalente de tu liquidación final."
)
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(footer_text, styles['Normal']))

    doc.build(elements)
