import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_header_styled(doc, text, level):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(6)
    for run in h.runs:
        run.font.name = 'Segoe UI'
        if level == 1:
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 41, 59) # Slate 800
        elif level == 2:
            run.font.size = Pt(13)
            run.font.bold = True
            run.font.color.rgb = RGBColor(71, 85, 105) # Slate 600
        elif level == 3:
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(100, 116, 139)
    return h

def add_paragraph_styled(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Segoe UI'
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    if text:
        r = p.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(10.5)
        r.font.italic = italic
        r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet_styled(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Segoe UI'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = 'Segoe UI'
    r.font.size = Pt(10)
    r.font.color.rgb = RGBColor(51, 65, 85)
    return p

def build_document():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Document Header / Brand Badge
    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_after = Pt(2)
    r_badge = p_badge.add_run("MEXADEV · PROYECTOS Y TECNOLOGÍA")
    r_badge.font.name = 'Segoe UI'
    r_badge.font.size = Pt(9)
    r_badge.font.bold = True
    r_badge.font.color.rgb = RGBColor(14, 165, 233) # Cyan/Sky 500

    # Main Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Bake Me Up: Sistema Web de Cotización Dinámica, Histórico y Gestión de Pedidos")
    r_title.font.name = 'Segoe UI'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Documento de Especificación Funcional, Plan de Migración desde Excel y Hoja de Ruta")
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(11.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # Metadata Box (Table)
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Cliente / Negocio:", "Bake Me Up (Sofia Gavito Alarcón)"),
        ("Consultoría & Desarrollo:", "MexaDev (Carlos Ruiz 'Woody' / Lalo)"),
        ("Fecha de Acuerdos:", "12 de octubre de 2026"),
        ("Estado de Documento:", "Versión 1.0 - Aprobado para levantamiento de fórmulas y migración")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.5)
        set_cell_background(c0, "F8FAFC")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.name = 'Segoe UI'
        r0.font.size = Pt(9.5)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(71, 85, 105)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = 'Segoe UI'
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1
    add_header_styled(doc, "1. Resumen Ejecutivo y Alcance del Proyecto", level=1)
    add_paragraph_styled(doc, "Bake Me Up opera actualmente su proceso de cotización y pedidos a través de múltiples hojas de cálculo (Exportek / Excel / Google Sheets). El crecimiento acelerado en el volumen de pedidos diarios, sumado a la volatilidad de los precios de los insumos de repostería (con fluctuaciones críticas como incrementos de hasta $200 en insumos básicos como el huevo), ha generado cuellos de botella operativos y desajustes de rentabilidad.")
    add_paragraph_styled(doc, "En la sesión estratégica celebrada el 12 de octubre de 2026, se acordó por decisión unánime la migración completa del proceso fuera de Excel para consolidarlo en un motor web centralizado e integrado dentro del portal de Bake Me Up. Este documento establece los lineamientos técnicos, las reglas de negocio y el procedimiento para procesar las hojas actuales y poner en marcha el sistema.")

    # Section 2
    add_header_styled(doc, "2. Diagnóstico Operativo: Desafíos Actuales vs. Solución Web", level=1)
    
    diag_table = doc.add_table(rows=6, cols=3)
    diag_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Aspecto", "Situación Actual (Excel / Hojas)", "Solución Propuesta (Motor Web Bake Me Up)"]
    for col_idx, h_text in enumerate(headers):
        cell = diag_table.rows[0].cells[col_idx]
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    rows_data = [
        ("Cálculo de Materias Primas", "Precios estáticos o dispersos; cuando un insumo sube, las fórmulas quedan desfasadas y se pierde margen.", "Matriz dinámica de costos: actualización centralizada que recalcula en cascada todas las recetas e históricos."),
        ("Consistencia de Cotización", "Diferentes integrantes del equipo cotizan con criterios variables; no hay estandarización.", "Motor algorítmico único: cualquier persona ingresa porciones y estilo, obteniendo exactamente el mismo precio oficial."),
        ("Betún y Mano de Obra", "Estimación empírica y manual de la cantidad de betún y horas requeridas por pastel.", "Estandarización por estilos (Vintage, Domo, Tradicional) con cálculo automático por porción."),
        ("Búsqueda Histórica", "Difícil localización de cotizaciones y diseños previos en carpetas o chats de WhatsApp.", "Catálogo histórico indexado con búsqueda por palabras clave, etiquetas y similitud de fotografías."),
        ("Agendamiento de Pedidos", "Uso simultáneo y fragmentado de Google Calendar, Notion y notas físicas de mostrador.", "Calendario unificado en el portal web: fecha, hora de entrega, anticipo pagado y saldo pendiente.")
    ]

    for row_idx, r_data in enumerate(rows_data, start=1):
        row = diag_table.rows[row_idx]
        bg_col = "FFFFFF" if row_idx % 2 != 0 else "F8FAFC"
        for col_idx, text in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = Inches(2.2) if col_idx > 0 else Inches(1.8)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = 'Segoe UI'
            r.font.size = Pt(9)
            if col_idx == 0:
                r.font.bold = True
            r.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Section 3
    add_header_styled(doc, "3. Especificación Funcional de Módulos", level=1)
    
    add_header_styled(doc, "3.1. Matriz Dinámica de Materias Primas (Insumos Base)", level=2)
    add_paragraph_styled(doc, "El corazón del sistema es la administración centralizada de costos de insumos:")
    add_bullet_styled(doc, "Catálogo de materias primas con unidad de medida (kg, lt, pza) y precio vigente de compra.", "Catálogo Base: ")
    add_bullet_styled(doc, "Al actualizar el precio del huevo, mantequilla, chocolate o harina, el sistema actualiza automáticamente el costo base de elaboración.", "Actualización en Cascada: ")
    add_bullet_styled(doc, "Para no castigar el margen y evitar cálculos excesivos al cotizar, la fórmula base asume el costeo de los insumos más costosos. De esta forma, cualquier combinación seleccionada por el cliente garantiza la rentabilidad deseada.", "Regla de Oro de Costeo: ")

    add_header_styled(doc, "3.2. Motor de Cotización Estandarizado (Web Quoting Engine)", level=2)
    add_paragraph_styled(doc, "Diseñado para ser operado en mostrador o respondiendo mensajes en menos de 60 segundos:")
    add_bullet_styled(doc, "Fecha y hora solicitada, número de personas/porciones.", "Paso 1 (Requerimiento): ")
    add_bullet_styled(doc, "Selección de estilo (ej. Vintage, Forma de Domo, Clásico, Pisos). El sistema calcula en automático gramos de betún y tiempo extra de trabajo.", "Paso 2 (Estilo y Complejidad): ")
    add_bullet_styled(doc, "Sabor de bizcocho y sabor de relleno seleccionados del catálogo.", "Paso 3 (Sabores): ")
    add_bullet_styled(doc, "Impresiones comestibles (obleas), flores (naturales/preservadas), letreros en papel o bases de MDF/acrílico.", "Paso 4 (Elementos Adicionales): ")
    add_bullet_styled(doc, "Costo Insumos + Mano de Obra + Gastos Operativos + Margen % = Precio Final Sugerido, con generación de resumen limpio para envío al cliente.", "Paso 5 (Cálculo Financiero): ")

    add_header_styled(doc, "3.3. Histórico Inteligente y Búsqueda Visual", level=2)
    add_bullet_styled(doc, "Búsqueda textual por diseño (ej. 'flores rosas', 'vintage perlas', 'domo bautizo').", "Búsqueda Semántica: ")
    add_bullet_styled(doc, "Capacidad de localizar pasteles similares cargando una foto o referencia visual.", "Búsqueda por Fotografía: ")
    add_bullet_styled(doc, "Permite abrir una cotización de hace meses y ver cuánto costó entonces vs. cuánto cuesta producirla hoy con los precios actuales.", "Comparador Histórico: ")

    add_header_styled(doc, "3.4. Calendario y Control de Pedidos", level=2)
    add_bullet_styled(doc, "Visualización de fechas saturadas vs. cupos disponibles de producción.", "Control de Capacidad: ")
    add_bullet_styled(doc, "Registro del anticipo cobrado (50% o monto libre) y cálculo del saldo pendiente a la entrega.", "Cobranza y Anticipos: ")
    add_bullet_styled(doc, "Sincronización técnica directa con Google Calendar para notificaciones operativas.", "Integración Operativa: ")

    # Section 4
    add_header_styled(doc, "4. Protocolo de Migración y Carga de Archivos de Excel", level=1)
    add_paragraph_styled(doc, "Para llevar a cabo la migración limpia de los libros actuales de Excel/Exportek, se ha dispuesto una estructura en la carpeta compartida de MEXADEV en Google Drive:")
    add_bullet_styled(doc, "G:\\Mi unidad\\MEXADEV\\05_Proyectos_y_Tecnologia\\BAKEMEUP\\00_Proceso_Actual_Excel\\", "Ruta de Carga de Excel Actual: ")
    add_bullet_styled(doc, "G:\\Mi unidad\\MEXADEV\\05_Proyectos_y_Tecnologia\\BAKEMEUP\\01_Especificacion_y_Propuesta\\", "Ruta de Documentación y Propuesta: ")
    
    add_paragraph_styled(doc, "Instrucciones para el equipo de Bake Me Up:")
    add_bullet_styled(doc, "Depositar en la carpeta '00_Proceso_Actual_Excel' la versión definitiva y corregida del archivo de Excel con el que operan hoy.", "1. Archivo Maestro: ")
    add_bullet_styled(doc, "Asegurarse de no incluir copias duplicadas ni respaldos intermedios.", "2. Depuración: ")
    add_bullet_styled(doc, "Verificar que contenga las listas actuales de insumos, gramos de betún por tamaño y costos de extras (MDF, flores, obleas).", "3. Parámetros Clave: ")

    # Section 5
    add_header_styled(doc, "5. Hoja de Ruta y Próximos Pasos Técnicos", level=1)
    roadmap_data = [
        ("Fase 1: Levantamiento y Extracción", "Subida de hojas de Excel a Drive, auditoría de fórmulas y validación de matriz de ingredientes."),
        ("Fase 2: Motor de Cálculo en Backend", "Construcción de la matriz dinámica de costos y cálculo automático de betún y mano de obra."),
        ("Fase 3: Interfaz Web y Catálogo", "Desarrollo del cotizador rápido en portal Bake Me Up, estandarización de estilos y formulario de mostrador."),
        ("Fase 4: Histórico y Búsqueda por Foto", "Indexación del historial, galería fotográfica y motor de búsqueda de referencias."),
        ("Fase 5: Calendario y Entrega Operativa", "Módulo de pedidos, anticipos, sincronización de calendario y capacitación al equipo.")
    ]
    for fase, desc in roadmap_data:
        add_bullet_styled(doc, desc, f"{fase}: ")

    doc.add_paragraph().paragraph_format.space_after = Pt(16)
    p_fin = doc.add_paragraph()
    r_fin = p_fin.add_run("Documento generado por MexaDev · Proyectos y Tecnología.")
    r_fin.font.name = 'Segoe UI'
    r_fin.font.size = Pt(9)
    r_fin.font.italic = True
    r_fin.font.color.rgb = RGBColor(148, 163, 184)

    output_path = r"G:\Mi unidad\MEXADEV\05_Proyectos_y_Tecnologia\BAKEMEUP\01_Especificacion_y_Propuesta\DOCUMENTO_TECNICO_COTIZADOR_Y_MIGRACION_BAKEMEUP.docx"
    doc.save(output_path)
    print("Document successfully created at:", output_path)

if __name__ == "__main__":
    build_document()
