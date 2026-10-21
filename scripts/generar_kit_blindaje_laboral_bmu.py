import os
import shutil
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Colores Oficiales de Marca Bake Me Up
COLOR_VERDE = RGBColor(83, 88, 57)      # #535839 (Verde Oliva oficial)
COLOR_CAFE = RGBColor(38, 18, 15)       # #26120f (Café Oscuro oficial)
COLOR_DORADO = RGBColor(208, 187, 125)  # #d0bb7d (Dorado oficial)
COLOR_GRIS = RGBColor(121, 135, 155)    # #79879b (Azul Gris Medio)
COLOR_MUTED = RGBColor(100, 116, 139)   # Slate gray

def set_cell_background(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'))

def set_cell_margins(cell, top=50, bottom=50, left=90, right=90):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), edge_data.get('val', 'single'))
            element.set(qn('w:sz'), str(edge_data.get('sz', 4)))
            element.set(qn('w:space'), '0')
            element.set(qn('w:color'), edge_data.get('color', 'auto'))
            tcBorders.append(element)
        else:
            tag = f'w:{edge}'
            element = OxmlElement(tag)
            element.set(qn('w:val'), 'none')
            tcBorders.append(element)
    tcPr.append(tcBorders)

def add_bmu_letterhead(doc, compact=False):
    """Agrega el encabezado membretado oficial y pie de página de Bake Me Up."""
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.45 if compact else 0.55)
    section.bottom_margin = Inches(0.45 if compact else 0.55)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    row = header_table.rows[0]
    cell_logo = row.cells[0]
    cell_text = row.cells[1]
    cell_logo.width = Inches(2.3)
    cell_text.width = Inches(4.8)

    logo_path = os.path.abspath(r'assets/images/logos/logo-header-verdeoliva.png')
    p_logo = cell_logo.paragraphs[0]
    p_logo.paragraph_format.space_after = Pt(0)
    p_logo.paragraph_format.space_before = Pt(0)
    r_logo = p_logo.add_run()
    if os.path.exists(logo_path):
        r_logo.add_picture(logo_path, width=Inches(1.65 if compact else 1.9))

    p_h1 = cell_text.paragraphs[0]
    p_h1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_h1.paragraph_format.space_after = Pt(1)
    p_h1.paragraph_format.space_before = Pt(2)
    r_h1 = p_h1.add_run("BAKE ME UP")
    r_h1.font.name = 'Segoe UI'
    r_h1.font.size = Pt(11.5 if compact else 12.5)
    r_h1.font.bold = True
    r_h1.font.color.rgb = COLOR_VERDE

    p_h2 = cell_text.add_paragraph()
    p_h2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_h2.paragraph_format.space_after = Pt(1)
    r_h2 = p_h2.add_run("Repostería Fina & Café de Especialidad")
    r_h2.font.name = 'Segoe UI'
    r_h2.font.size = Pt(8)
    r_h2.font.italic = True
    r_h2.font.color.rgb = COLOR_GRIS

    p_h3 = cell_text.add_paragraph()
    p_h3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_h3.paragraph_format.space_after = Pt(0)
    r_h3 = p_h3.add_run("Titular: Ing. Sofía Gavito Alarcón · RFC: GAAS0208311X9\nAv. Municipio Libre 1972, Local 8, Puebla, Pue. · bakemeup.mx")
    r_h3.font.name = 'Segoe UI'
    r_h3.font.size = Pt(7)
    r_h3.font.color.rgb = COLOR_MUTED

    # Pleca divisoria
    divider_table = doc.add_table(rows=1, cols=1)
    divider_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_div = divider_table.rows[0].cells[0]
    c_div.width = Inches(7.1)
    set_cell_background(c_div, "535839")
    set_cell_margins(c_div, top=10, bottom=10, left=0, right=0)
    p_div = c_div.paragraphs[0]
    p_div.paragraph_format.space_after = Pt(0)
    p_div.paragraph_format.space_before = Pt(0)
    r_div = p_div.add_run("")
    r_div.font.size = Pt(1)

    # Footer
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.space_after = Pt(0)
    
    r_ft_line = footer_p.add_run("―" * 50 + "\n")
    r_ft_line.font.name = 'Segoe UI'
    r_ft_line.font.size = Pt(6.5)
    r_ft_line.font.color.rgb = COLOR_DORADO

    r_ft1 = footer_p.add_run("Bake Me Up · Domicilio Fiscal y Centro de Trabajo: Av. Municipio Libre 1972, Local 8, Col. Ex-Hacienda Mayorazgo, C.P. 72480, Puebla, Pue. (Plaza Pabellón Las Torres)\n")
    r_ft1.font.name = 'Segoe UI'
    r_ft1.font.size = Pt(6.5)
    r_ft1.font.color.rgb = COLOR_MUTED

    r_ft2 = footer_p.add_run("Documento Laboral Interno · bakemeup.mx · Repostería Fina & Café de Especialidad")
    r_ft2.font.name = 'Segoe UI'
    r_ft2.font.size = Pt(6.5)
    r_ft2.font.bold = True
    r_ft2.font.color.rgb = COLOR_VERDE


def add_p(doc, text="", bold_prefix="", size=8.5, space_before=2, space_after=4, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Segoe UI'
        rb.font.size = Pt(size)
        rb.font.bold = True
        rb.font.color.rgb = COLOR_VERDE
    if text:
        r = p.add_run(text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(size)
        r.font.color.rgb = COLOR_CAFE
    return p


# ==============================================================================
# 1. FORMATO DE CONTRATO INDIVIDUAL DE TRABAJO CORREGIDO Y BLINDADO
# ==============================================================================
def build_contrato_maestro():
    doc = Document()
    add_bmu_letterhead(doc, compact=True)

    p_title = add_p(doc, "", "CONTRATO INDIVIDUAL DE TRABAJO POR TIEMPO INDETERMINADO (CON PERIODO INICIAL A PRUEBA)", size=10, space_before=6, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc,
        "Contrato Individual de Trabajo que celebran, por una parte, la ING. SOFÍA GAVITO ALARCÓN, en su carácter de Persona Física con Actividad Empresarial y titular del establecimiento comercial denominado \"BAKE ME UP\", a quien en lo sucesivo se le denominará \"LA EMPLEADORA\"; y por la otra parte, por su propio derecho, C. _____________________________________________________, a quien en lo sucesivo se le denominará \"EL/LA TRABAJADOR(A)\", al tenor de las siguientes Declaraciones y Cláusulas:",
        size=8.5, space_after=4
    )

    add_p(doc, "", "DECLARACIONES", size=9, space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc,
        "Ser persona física mexicana, mayor de edad, con RFC GAAS0208311X9 y CURP GAAS020831MPLVLFA1, señalando como domicilio fiscal y centro de trabajo el ubicado en AVENIDA MUNICIPIO LIBRE 1972, LOCAL 8, COLONIA EX-HACIENDA MAYORAZGO, C.P. 72480, PUEBLA, PUEBLA (PLAZA PABELLÓN LAS TORRES), dedicada al giro de repostería fina artesanal y cafetería de especialidad.",
        "I. Declara \"LA EMPLEADORA\": ", size=8
    )

    add_p(doc,
        "Llamarse como ha quedado escrito, de nacionalidad mexicana, mayor de edad, con CURP ________________________________, RFC _______________________, y domicilio particular en __________________________________________________________________________________________, C.P. ___________, en Puebla, Pue.; manifestando contar con la capacidad, experiencia, higiene y aptitudes necesarias para desempeñar el puesto de: _____________________________________________.",
        "II. Declara \"EL/LA TRABAJADOR(A)\": ", size=8
    )

    add_p(doc, "", "CLÁUSULAS", size=9, space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)

    clausulas = [
        ("PRIMERA. MODALIDAD Y PERIODO A PRUEBA (ART. 35 Y 39-A LFT): ",
         "El presente contrato se celebra por TIEMPO INDETERMINADO, sujetándose en su inicio a un PERIODO A PRUEBA DE 30 DÍAS NATURALES, comprendido del día _____ de _________________ al día _____ de _________________ de 202___, conforme al artículo 39-A de la Ley Federal del Trabajo, con el único fin de verificar que \"EL/LA TRABAJADOR(A)\" cumple con los requisitos, disciplina, apego a recetas, higiene (NOM-251) y conocimientos necesarios. Si al concluir los 30 días acredita satisfactoriamente su evaluación, la relación continuará por tiempo indeterminado; de lo contrario, se dará por terminada sin responsabilidad para \"LA EMPLEADORA\"."),
        ("SEGUNDA. PUESTO, LUGAR Y FUNCIONES (ART. 25 FRACC. III Y IV LFT): ",
         "\"EL/LA TRABAJADOR(A)\" prestará sus servicios personales subordinados en el domicilio del centro de trabajo de \"LA EMPLEADORA\" (Av. Municipio Libre 1972, Local 8, Puebla, Pue.), desempeñando el puesto de _______________________________________, obligándose de manera enunciativa mas no limitativa a: preparación de alimentos/bebidas conforme a recetarios, atención a clientes, abastecimiento de estación y ejecución estricta del Rol Diario de Limpieza e Higiene del establecimiento."),
        ("TERCERA. JORNADA DE TRABAJO Y HORARIO (ART. 58, 59 Y 61 LFT): ",
         "La jornada laboral pactada será de modalidad: [  ] TIEMPO COMPLETO (8 horas diarias)  /  [  ] JORNADA REDUCIDA DE MEDIO TIEMPO (4 horas diarias), laborando _____ días a la semana, en un horario de las _______:_______ a las _______:_______ horas. Queda expresamente pactado conforme al Art. 59 LFT que \"LA EMPLEADORA\" podrá ajustar el rol de turnos según las necesidades operativas de la cafetería sin exceder los máximos legales."),
        ("CUARTA. PROHIBICIÓN DE HORAS EXTRAS SIN ORDEN ESCRITA (ART. 66 LFT): ",
         "Queda estrictamente prohibido para \"EL/LA TRABAJADOR(A)\" permanecer en el centro de trabajo o laborar tiempo extraordinario después de concluida su jornada sin contar con autorización previa y por escrito firmada por \"LA EMPLEADORA\", requisito sin el cual no se reconocerá tiempo extraordinario alguno. \"EL/LA TRABAJADOR(A)\" se obliga a registrar diariamente su hora exacta de entrada y salida en la Bitácora de Asistencia."),
        ("QUINTA. SALARIO Y FORMA DE PAGO (ART. 82, 83 Y 101 LFT): ",
         "Como retribución por sus servicios, \"EL/LA TRABAJADOR(A)\" percibirá un salario mensual de $__________________ MXN (_____________________________________________________ pesos 00/100 M.N.), el cual incluye íntegramente el pago proporcional de los séptimos días (descansos semanales). El pago se cubrirá de forma quincenal los días 15 y último de cada mes, en moneda de curso legal o mediante transferencia electrónica bancaria, obligándose \"EL/LA TRABAJADOR(A)\" a firmar en cada pago el Recibo Quincenal de Nómina correspondiente."),
        ("SEXTA. NATURALEZA DE LAS PROPINAS (ART. 346 Y 347 LFT): ",
         "Las partes reconocen que las propinas que voluntariamente dejen los clientes en el establecimiento son gratificaciones eventuales y variables ajenas a \"LA EMPLEADORA\", las cuales son concentradas y repartidas proporcionalmente entre el propio personal operativo según sus turnos efectivamente laborados, por lo que no constituyen un monto fijo garantizado por el negocio."),
        ("SÉPTIMA. DÍA DE DESCANSO, VACACIONES Y AGUINALDO (ART. 69, 74, 76, 80 Y 87 LFT): ",
         "\"EL/LA TRABAJADOR(A)\" disfrutará de su descanso semanal con goce de sueldo (preferentemente en día domingo o según rol acordado), así como de los días de descanso obligatorio previstos en el Art. 74 de la LFT, vacaciones anuales dignas (mínimo 12 días el primer año conforme al Art. 76 LFT), prima vacacional del 25% y un aguinaldo anual equivalente a 15 días de salario (o su parte proporcional) pagadero antes del 20 de diciembre."),
        ("OCTAVA. CONFIDENCIALIDAD Y PROPIEDAD DE RECETAS (ART. 134 FRACC. XIII LFT): ",
         "\"EL/LA TRABAJADOR(A)\" reconoce que todas las recetas, gramajes, fórmulas de repostería, costos, listas de proveedores y bases de datos de clientes son propiedad intelectual y secreto industrial exclusivo de \"BAKE ME UP\", obligándose a no divulgarlos, fotografiarlos, sustraerlos ni reproducirlos en beneficio propio o de terceros, aun después de terminada la relación laboral."),
        ("NOVENA. REGLAMENTO INTERIOR Y CAUSALES DE RESCISIÓN (ART. 47 Y 423 LFT): ",
         "\"EL/LA TRABAJADOR(A)\" manifiesta haber leído, recibido y firmado de conformidad el Reglamento Interior de Trabajo de \"BAKE ME UP\", obligándose a acatar sus disposiciones de puntualidad, inocuidad alimentaria (NOM-251), no uso de celular en operación y respeto, aceptando las medidas disciplinarias y causales de rescisión sin responsabilidad patronal previstas en el artículo 47 de la LFT (incluyendo acumular más de 3 faltas injustificadas en un periodo de 30 días)."),
        ("DÉCIMA. DESIGNACIÓN DE BENEFICIARIOS (ART. 25 FRACC. X Y 501 LFT): ",
         "Para el pago de salarios y prestaciones devengadas no cobradas en caso de fallecimiento o desaparición, \"EL/LA TRABAJADOR(A)\" designa como beneficiario(a) en un 100% a: _______________________________________________________, con parentesco: _______________________ y teléfono: _______________________.")
    ]

    for b_pre, txt in clausulas:
        add_p(doc, txt, b_pre, size=7.8, space_before=1.5, space_after=2.5)

    add_p(doc,
        "Leído que fue el presente Contrato Individual de Trabajo y enteradas las partes de su contenido, valor y fuerza legal, lo firman y estampan su huella digital por duplicado al margen y al calce en la Heroica Puebla de Zaragoza, a los _____ días del mes de ___________________ del año 2026.",
        size=8, space_before=4, space_after=8
    )

    # Bloque de firmas y huella
    sig_table = doc.add_table(rows=1, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False
    c_pat, c_trab, c_huella = sig_table.rows[0].cells
    c_pat.width = Inches(2.8)
    c_trab.width = Inches(2.9)
    c_huella.width = Inches(1.4)

    p1 = c_pat.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p1.add_run("POR \"LA EMPLEADORA\"\n\n\n____________________________________\nING. SOFÍA GAVITO ALARCÓN\nTitular · Bake Me Up")
    r1.font.name = 'Segoe UI'
    r1.font.size = Pt(8)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_CAFE

    p2 = c_trab.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("POR \"EL/LA TRABAJADOR(A)\"\n\n\n____________________________________\nNombre y Firma de Conformidad\nRecibí ejemplar original")
    r2.font.name = 'Segoe UI'
    r2.font.size = Pt(8)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_CAFE

    set_cell_border(c_huella, top={'val':'single','sz':4,'color':'535839'}, bottom={'val':'single','sz':4,'color':'535839'}, left={'val':'single','sz':4,'color':'535839'}, right={'val':'single','sz':4,'color':'535839'})
    ph = c_huella.paragraphs[0]
    ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rh = ph.add_run("\n\n\n\nHUELLA DIGITAL\nPulgar Derecho")
    rh.font.name = 'Segoe UI'
    rh.font.size = Pt(6.5)
    rh.font.color.rgb = COLOR_MUTED

    return doc


# ==============================================================================
# 2. FORMATO DE RECIBO QUINCENAL DE NÓMINA Y PROPINAS (2 POR HOJA CARTA)
# ==============================================================================
def build_recibo_quincenal():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.35)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.6)
    section.right_margin = Inches(0.6)

    for idx_recibo in range(2):
        # Encabezado compacto del recibo
        hdr = doc.add_table(rows=1, cols=2)
        hdr.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr.autofit = False
        c0, c1 = hdr.rows[0].cells
        c0.width = Inches(4.5)
        c1.width = Inches(2.8)
        set_cell_background(c0, "535839")
        set_cell_background(c1, "535839")
        set_cell_margins(c0, top=40, bottom=40, left=80, right=60)
        set_cell_margins(c1, top=40, bottom=40, left=60, right=80)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run("BAKE ME UP · RECIBO QUINCENAL DE PAGO DE SALARIO Y PRESTACIONES")
        r0.font.name = 'Segoe UI'
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(255, 255, 255)

        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run("RFC: GAAS0208311X9 · Puebla, Pue.")
        r1.font.name = 'Segoe UI'
        r1.font.size = Pt(7.5)
        r1.font.color.rgb = RGBColor(245, 223, 172)

        # Tabla de datos del colaborador y desglose
        tbl = doc.add_table(rows=6, cols=4)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        rows_spec = [
            ("Colaborador(a):", "_______________________________________", "Periodo Quincenal:", "Del ____ al ____ de ____________ 2026"),
            ("Puesto / Jornada:", "[ ] Completo (8h)   [ ] Medio Tiempo (4h)", "Días Trabajados:", "______ días (Incluye 7° día pagado)"),
            ("1. Sueldo Quincenal Base:", "$ ____________________ MXN", "2. Descuento por Faltas:", "- $ ____________________ MXN (____ faltas)"),
            ("3. Horas Extra Pagadas:", "+ $ ____________________ MXN (____ hrs)", "4. SUELDO NETO PAGADO:", "$ ______________________ MXN"),
            ("5. Reparto de Propinas*:", "$ ____________________ MXN (Efectivo)", "Forma de Pago Sueldo:", "[ ] Transferencia    [ ] Efectivo"),
            ("TOTAL RECIBIDO EN MANO:", "$ ______________________ MXN", "Importe Total en Letra:", "( ________________________________________ )")
        ]

        widths = [Inches(1.55), Inches(2.2), Inches(1.55), Inches(2.0)]
        for r_idx, (k1, v1, k2, v2) in enumerate(rows_spec):
            row = tbl.rows[r_idx]
            vals = [k1, v1, k2, v2]
            for c_idx, val in enumerate(vals):
                cell = row.cells[c_idx]
                cell.width = widths[c_idx]
                bg = "F8F9F6" if r_idx in (3, 5) else "FFFFFF"
                set_cell_background(cell, bg)
                set_cell_margins(cell, top=30, bottom=30, left=50, right=50)
                set_cell_border(cell,
                    top={'val':'single','sz':4,'color':'535839'} if r_idx==0 else {'val':'dotted','sz':2,'color':'D0BB7D'},
                    bottom={'val':'single','sz':4,'color':'535839'} if r_idx==5 else {'val':'dotted','sz':2,'color':'D0BB7D'},
                    left={'val':'single','sz':4,'color':'535839'} if c_idx==0 else {'val':'dotted','sz':2,'color':'D0BB7D'},
                    right={'val':'single','sz':4,'color':'535839'} if c_idx==3 else {'val':'dotted','sz':2,'color':'D0BB7D'}
                )
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.space_before = Pt(0)
                r = p.add_run(val)
                r.font.name = 'Segoe UI'
                r.font.size = Pt(7.5)
                if c_idx in (0, 2):
                    r.font.bold = True
                    r.font.color.rgb = COLOR_VERDE if r_idx in (3, 5) else COLOR_CAFE
                else:
                    r.font.color.rgb = COLOR_CAFE

        # Declaración liberatoria y firma
        sig_tbl = doc.add_table(rows=1, cols=3)
        sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        sig_tbl.autofit = False
        sc0, sc1, sc2 = sig_tbl.rows[0].cells
        sc0.width = Inches(4.2)
        sc1.width = Inches(2.1)
        sc2.width = Inches(1.0)

        for sc in (sc0, sc1, sc2):
            set_cell_margins(sc, top=35, bottom=35, left=50, right=50)
            set_cell_border(sc, top={'val':'none'}, bottom={'val':'single','sz':4,'color':'535839'}, left={'val':'single','sz':4,'color':'535839'}, right={'val':'single','sz':4,'color':'535839'})

        ps0 = sc0.paragraphs[0]
        ps0.paragraph_format.space_after = Pt(0)
        ps0.paragraph_format.line_spacing = 1.05
        rs0 = ps0.add_run(
            "DECLARACIÓN DE CONFORMIDAD Y NO ADEUDO: Recibí de Ing. Sofía Gavito Alarcón (Bake Me Up) la cantidad neta arriba descrita, "
            "manifestando bajo protesta de decir verdad que a la fecha se me han cubierto íntegramente mis salarios ordinarios, séptimos días, "
            "descansos y tiempo extraordinario en caso de haberlo laborado, sin que se me adeude cantidad alguna por ningún concepto.\n"
            "*Nota (Art. 346 LFT): Las propinas corresponden al reparto proporcional de gratificaciones voluntarias de clientes."
        )
        rs0.font.name = 'Segoe UI'
        rs0.font.size = Pt(6.5)
        rs0.font.color.rgb = COLOR_CAFE

        ps1 = sc1.paragraphs[0]
        ps1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ps1.paragraph_format.space_after = Pt(0)
        rs1 = ps1.add_run("RECIBÍ DE CONFORMIDAD\n\n\n_______________________________\nFirma Autógrafa y Fecha")
        rs1.font.name = 'Segoe UI'
        rs1.font.size = Pt(7)
        rs1.font.bold = True
        rs1.font.color.rgb = COLOR_CAFE

        ps2 = sc2.paragraphs[0]
        ps2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ps2.paragraph_format.space_after = Pt(0)
        rs2 = ps2.add_run("\n\n\nHUELLA\nPulgar Der.")
        rs2.font.name = 'Segoe UI'
        rs2.font.size = Pt(6)
        rs2.font.color.rgb = COLOR_MUTED

        if idx_recibo == 0:
            p_cut = doc.add_paragraph()
            p_cut.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cut.paragraph_format.space_before = Pt(10)
            p_cut.paragraph_format.space_after = Pt(10)
            rcut = p_cut.add_run("✂  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
            rcut.font.name = 'Segoe UI'
            rcut.font.size = Pt(7.5)
            rcut.font.color.rgb = COLOR_GRIS

    return doc


# ==============================================================================
# 3. FORMATO DE BITÁCORA QUINCENAL DE ASISTENCIA Y HORARIOS
# ==============================================================================
def build_bitacora_asistencia():
    doc = Document()
    add_bmu_letterhead(doc, compact=True)

    add_p(doc, "", "BITÁCORA OFICIAL DE CONTROL DE ASISTENCIA, PUNTUALIDAD Y JORNADA LABORAL", size=9.5, space_before=4, space_after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p(doc, "Periodo Quincenal: Del _____ al _____ de ______________________ de 2026   |   Sucursal: Plaza Pabellón Las Torres", size=8, space_before=0, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)

    tbl = doc.add_table(rows=21, cols=7)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    headers = ["Fecha", "Nombre del Colaborador(a)", "Hora Entrada", "Salida Comida", "Regreso Comida", "Hora Salida", "Firma de Conformidad"]
    col_widths = [Inches(0.75), Inches(1.85), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8), Inches(1.3)]

    hdr_row = tbl.rows[0]
    for idx, h_text in enumerate(headers):
        c = hdr_row.cells[idx]
        c.width = col_widths[idx]
        set_cell_background(c, "535839")
        set_cell_margins(c, top=40, bottom=40, left=30, right=30)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = 'Segoe UI'
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    for r_idx in range(1, 21):
        row = tbl.rows[r_idx]
        bg = "F8F9F6" if r_idx % 2 == 0 else "FFFFFF"
        for c_idx in range(7):
            c = row.cells[c_idx]
            c.width = col_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=45, bottom=45, left=30, right=30)
            set_cell_border(c,
                top={'val':'single','sz':3,'color':'D0BB7D'},
                bottom={'val':'single','sz':4,'color':'535839'} if r_idx==20 else {'val':'single','sz':3,'color':'D0BB7D'},
                left={'val':'single','sz':3,'color':'535839'},
                right={'val':'single','sz':3,'color':'535839'}
            )
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(" ")
            r.font.size = Pt(8)

    add_p(doc,
        "Al firmar mi registro diario, reconozco que las horas asentadas corresponden fielmente a mi jornada real laborada. Conforme al Artículo 66 de la Ley Federal del Trabajo y al Reglamento Interior de Trabajo de Bake Me Up, queda estrictamente prohibido laborar tiempo extraordinario sin orden previa y por escrito firmada por la Dirección General.",
        "NOTA LEGAL OBLIGATORIA: ", size=7.5, space_before=6, space_after=2
    )

    return doc


# ==============================================================================
# 4. FORMATO DE ACTA ADMINISTRATIVA OFICIAL (FALTAS, RETARDOS Y ABANDONO)
# ==============================================================================
def build_acta_administrativa():
    doc = Document()
    add_bmu_letterhead(doc, compact=True)

    add_p(doc, "", "ACTA ADMINISTRATIVA LABORAL E INSTRUMENTACIÓN DE HECHOS", size=10, space_before=6, space_after=4, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc,
        "En la Heroica Puebla de Zaragoza, siendo las _______:_______ horas del día _____ del mes de ___________________ del año 2026, reunidos en las instalaciones del centro de trabajo \"BAKE ME UP\", ubicado en Avenida Municipio Libre 1972, Local 8, Colonia Ex-Hacienda Mayorazgo, C.P. 72480, Puebla, Pue., comparecen: por parte de la Dirección General, la ING. SOFÍA GAVITO ALARCÓN; el/la colaborador(a) involucrado(a) C. _____________________________________________________, quien ocupa el puesto de _____________________________________; así como dos testigos de asistencia, C. _____________________________________________ y C. _____________________________________________, a efecto de hacer constar los siguientes:",
        size=8.2, space_after=4
    )

    # Tabla de hechos y fundamentos
    tbl = doc.add_table(rows=4, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    secciones = [
        ("1. MOTIVO DEL ACTA ADMINISTRATIVA (Marcar con 'X'):",
         "[  ] Falta(s) Injustificada(s) de Asistencia (Fecha de la falta: ____/____/2026 — Acumuladas en 30 días: ____ faltas)\n"
         "[  ] Acumulación de 3 o más Retardos en un periodo de 30 días naturales\n"
         "[  ] Incumplimiento de Obligaciones Operativas, Rol de Limpieza o Abastecimiento de Estación\n"
         "[  ] Violación a Normas de Higiene e Inocuidad Alimentaria (NOM-251) o Desapego a Recetas Oficiales\n"
         "[  ] Constancia de Inasistencia / Abandono de Empleo (El trabajador no se presentó a su turno sin aviso ni justificación)"),
        ("2. RELACIÓN DETALLADA DE LOS HECHOS (Día, hora y descripción objetiva):",
         "____________________________________________________________________________________________________________________________\n"
         "____________________________________________________________________________________________________________________________\n"
         "____________________________________________________________________________________________________________________________"),
        ("3. MANIFESTACIÓN DEL COLABORADOR(A) (Uso de la palabra o constancia de no comparecencia):",
         "____________________________________________________________________________________________________________________________\n"
         "____________________________________________________________________________________________________________________________"),
        ("4. DETERMINACIÓN Y MEDIDA DISCIPLINARIA APLICADA (Art. 47 y 423 Fracc. X LFT y Reglamento Interior):",
         "[  ] Amonestación Escrita en Expediente    [  ] Suspensión de ____ día(s) sin goce de sueldo (Fechas: _____________________)\n"
         "[  ] Cómputo de Falta Injustificada para efectos del Art. 47 Fracc. X de la LFT (Más de 3 faltas en 30 días = Rescisión Justificada)")
    ]

    for idx, (tit, body) in enumerate(secciones):
        cell = tbl.rows[idx].cells[0]
        cell.width = Inches(7.1)
        set_cell_background(cell, "F8F9F6")
        set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
        set_cell_border(cell,
            top={'val':'single','sz':4,'color':'535839'},
            bottom={'val':'single','sz':4,'color':'535839'},
            left={'val':'single','sz':4,'color':'535839'},
            right={'val':'single','sz':4,'color':'535839'}
        )
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        rt = p.add_run(tit + "\n")
        rt.font.name = 'Segoe UI'
        rt.font.size = Pt(8)
        rt.font.bold = True
        rt.font.color.rgb = COLOR_VERDE

        rb = p.add_run(body)
        rb.font.name = 'Segoe UI'
        rb.font.size = Pt(7.8)
        rb.font.color.rgb = COLOR_CAFE

    add_p(doc,
        "No habiendo más hechos que hacer constar, se cierra la presente acta siendo las _______:_______ horas del mismo día, firmando al calce los que en ella intervinieron. En caso de que el/la colaborador(a) no se encuentre presente por inasistencia o se niegue a firmar, los dos testigos hacen constar dicho hecho con su firma autógrafa para todos los efectos legales ante el Centro de Conciliación Laboral y Tribunales Laborales.",
        size=8, space_before=6, space_after=8
    )

    sig_tbl = doc.add_table(rows=2, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_tbl.autofit = False

    firmantes = [
        ("POR LA EMPRESA / DIRECCIÓN\n\n\n_________________________________________\nING. SOFÍA GAVITO ALARCÓN\nDirección General · Bake Me Up",
         "EL / LA COLABORADOR(A)\n\n\n_________________________________________\nNombre y Firma (o constancia de negativa/ausencia)\n[  ] Se negó a firmar   [  ] Ausente por falta"),
        ("\nTESTIGO DE ASISTENCIA 1\n\n\n_________________________________________\nNombre Completo y Firma",
         "\nTESTIGO DE ASISTENCIA 2\n\n\n_________________________________________\nNombre Completo y Firma")
    ]

    for r_i in range(2):
        for c_i in range(2):
            c = sig_tbl.rows[r_i].cells[c_i]
            c.width = Inches(3.55)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(firmantes[r_i][c_i])
            r.font.name = 'Segoe UI'
            r.font.size = Pt(7.8)
            r.font.bold = True
            r.font.color.rgb = COLOR_CAFE

    return doc


# ==============================================================================
# 5. FORMATO DE CARTA DE RENUNCIA VOLUNTARIA Y CONVENIO DE FINIQUITO
# ==============================================================================
def build_renuncia_y_finiquito():
    doc = Document()
    add_bmu_letterhead(doc, compact=True)

    # --- PÁGINA 1: CARTA DE RENUNCIA VOLUNTARIA ---
    add_p(doc, "Puebla, Pue., a _____ de ___________________ de 2026\nASUNTO: RENUNCIA VOLUNTARIA E IRREVOCABLE Y CONSTANCIA DE NO ADEUDO", size=8.5, space_before=6, space_after=6, align=WD_ALIGN_PARAGRAPH.RIGHT)

    add_p(doc, "ING. SOFÍA GAVITO ALARCÓN\nTITULAR Y DIRECTORA GENERAL DE \"BAKE ME UP\"\nP R E S E N T E .", size=9, space_before=2, space_after=8, align=WD_ALIGN_PARAGRAPH.LEFT)

    add_p(doc,
        "Por medio de la presente, yo, C. _________________________________________________________, por mi propio derecho y por así convenir exclusivamente a mis intereses personales y profesionales, presento ante usted mi RENUNCIA VOLUNTARIA CON CARÁCTER DE IRREVOCABLE al puesto de _________________________________________ que venía desempeñando en el establecimiento comercial denominado \"BAKE ME UP\", dando por terminada de forma libre, espontánea y por mutuo consentimiento la relación y el Contrato Individual de Trabajo que me unía con usted, con efectos a partir del día de hoy, _____ de ___________________ de 2026, de conformidad con el artículo 53 fracción I de la Ley Federal del Trabajo.",
        size=8.8, space_before=4, space_after=6
    )

    add_p(doc,
        "Asimismo, manifiesto expresamente y bajo protesta de decir verdad que durante todo el tiempo en que presté mis servicios para \"BAKE ME UP\" (desde mi fecha de ingreso el día _____ de ___________________ de 202___ hasta el día de hoy), recibí siempre de manera puntual e íntegra el pago de mis salarios ordinarios, séptimos días, días de descanso obligatorio, vacaciones, prima vacacional, aguinaldo y demás prestaciones legales y contractuales a las que tuve derecho, sin haber laborado tiempo extraordinario que no me haya sido cubierto en su oportunidad.",
        size=8.8, space_before=2, space_after=6
    )

    add_p(doc,
        "De igual forma, hago constar que durante la vigencia de mi relación laboral jamás sufrí accidente de trabajo ni contraje enfermedad profesional alguna, por lo que en este acto otorgo a favor de la ING. SOFÍA GAVITO ALARCÓN y/o \"BAKE ME UP\" el FINIQUITO MÁS AMPLIO Y LIBERATORIO que en derecho proceda, no reservándome acción ni derecho alguno de carácter laboral, civil, administrativo o de cualquier otra naturaleza que ejercitar en su contra en el presente o en el futuro.",
        size=8.8, space_before=2, space_after=6
    )

    add_p(doc,
        "Agradezco las atenciones, el apoyo y la oportunidad de crecimiento brindada durante el tiempo que formé parte de este equipo de trabajo, ratificando que firmo y estampo mi huella digital en la presente renuncia sin que medie coacción, presión, dolo ni violencia de ningún tipo.",
        size=8.8, space_before=2, space_after=14
    )

    sig_r = doc.add_table(rows=1, cols=2)
    sig_r.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_r.autofit = False
    cr0, cr1 = sig_r.rows[0].cells
    cr0.width = Inches(5.3)
    cr1.width = Inches(1.6)

    pr0 = cr0.paragraphs[0]
    pr0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr0 = pr0.add_run(
        "ATENTAMENTE Y POR MI PROPIO DERECHO\n\n\n\n____________________________________________________________\n"
        "C. _________________________________________________________\n"
        "Nombre Completo y Firma Autógrafa de Puño y Letra\n"
        "(Escribir de puño y letra: \"Renuncio voluntariamente y no se me adeuda nada\")"
    )
    rr0.font.name = 'Segoe UI'
    rr0.font.size = Pt(8.5)
    rr0.font.bold = True
    rr0.font.color.rgb = COLOR_CAFE

    set_cell_border(cr1, top={'val':'single','sz':4,'color':'535839'}, bottom={'val':'single','sz':4,'color':'535839'}, left={'val':'single','sz':4,'color':'535839'}, right={'val':'single','sz':4,'color':'535839'})
    pr1 = cr1.paragraphs[0]
    pr1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rr1 = pr1.add_run("\n\n\n\n\nHUELLA DIGITAL\nPulgar Derecho")
    rr1.font.name = 'Segoe UI'
    rr1.font.size = Pt(7)
    rr1.font.color.rgb = COLOR_MUTED

    # Salto de página para la Hoja 2: Recibo Desglosado de Finiquito
    doc.add_page_break()

    # --- PÁGINA 2: RECIBO DESGLOSADO DE FINIQUITO ---
    add_p(doc, "", "CONVENIO DE TERMINACIÓN Y RECIBO DESGLOSADO DE FINIQUITO LABORAL", size=10, space_before=6, space_after=6, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_p(doc,
        "Bueno por: $ ______________________ MXN\n"
        "Con fecha _____ de ___________________ de 2026, recibí de la ING. SOFÍA GAVITO ALARCÓN (\"BAKE ME UP\") la cantidad neta de "
        "$ ______________________ MXN (_____________________________________________________________________ pesos ___/100 M.N.), "
        "por concepto de PAGO TOTAL Y DEFINITIVO DE FINIQUITO derivado de mi renuncia voluntaria, conforme al siguiente desglose de prestaciones proporcionales:",
        size=8.5, space_after=6
    )

    fin_tbl = doc.add_table(rows=7, cols=3)
    fin_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    fin_tbl.autofit = False

    fin_rows = [
        ("CONCEPTO DE FINIQUITO", "DIAS / PROPORCIÓN", "IMPORTE EN PESOS (MXN)"),
        ("1. Días laborados pendientes de la quincena en curso", "______ días laborados", "$ ______________________ MXN"),
        ("2. Aguinaldo Proporcional (Base 15 días al año - Art. 87 LFT)", "______ días prop.", "$ ______________________ MXN"),
        ("3. Vacaciones Proporcionales no disfrutadas (Art. 76 y 79 LFT)", "______ días prop.", "$ ______________________ MXN"),
        ("4. Prima Vacacional Proporcional (25% sobre vacaciones - Art. 80 LFT)", "25% de ley", "$ ______________________ MXN"),
        ("5. Reparto pendiente de propinas / Otros conceptos a favor", "Liquidación a la fecha", "$ ______________________ MXN"),
        ("TOTAL NETO DEL FINIQUITO PAGADO Y RECIBIDO:", "PAGO ÚNICO TOTAL", "$ ______________________ MXN")
    ]

    f_widths = [Inches(3.6), Inches(1.6), Inches(1.9)]
    for r_i, (col0, col1, col2) in enumerate(fin_rows):
        row = fin_tbl.rows[r_i]
        for c_i, val in enumerate([col0, col1, col2]):
            c = row.cells[c_i]
            c.width = f_widths[c_i]
            bg = "535839" if r_i == 0 else ("F8F9F6" if r_i == 6 else "FFFFFF")
            set_cell_background(c, bg)
            set_cell_margins(c, top=45, bottom=45, left=60, right=60)
            set_cell_border(c,
                top={'val':'single','sz':4,'color':'535839'},
                bottom={'val':'single','sz':4,'color':'535839'},
                left={'val':'single','sz':4,'color':'535839'},
                right={'val':'single','sz':4,'color':'535839'}
            )
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.name = 'Segoe UI'
            r.font.size = Pt(8)
            if r_i == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_i == 6:
                r.font.bold = True
                r.font.color.rgb = COLOR_VERDE if c_i == 0 else COLOR_CAFE
            else:
                r.font.color.rgb = COLOR_CAFE

    add_p(doc,
        "Forma de entrega del pago:   [  ] Efectivo en mano     [  ] Transferencia Bancaria (Folio/Rastreo: ___________________________)\n\n"
        "Al recibir el importe total antes descrito a mi entera satisfacción, ratifico mi renuncia voluntaria y manifiesto que la relación laboral ha concluido sin que exista adeudo alguno por salarios devengados, descansos, tiempo extraordinario, reparto de utilidades ni ninguna otra prestación legal, otorgando recibo de finiquito total y definitivo.",
        size=8.5, space_before=8, space_after=14
    )

    sig_f = doc.add_table(rows=1, cols=3)
    sig_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_f.autofit = False
    cf0, cf1, cf2 = sig_f.rows[0].cells
    cf0.width = Inches(2.7)
    cf1.width = Inches(2.9)
    cf2.width = Inches(1.5)

    pf0 = cf0.paragraphs[0]
    pf0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rf0 = pf0.add_run("ENTREGÓ FINIQUITO (EMPRESA)\n\n\n\n___________________________________\nING. SOFÍA GAVITO ALARCÓN\nTitular · Bake Me Up")
    rf0.font.name = 'Segoe UI'
    rf0.font.size = Pt(8)
    rf0.font.bold = True
    rf0.font.color.rgb = COLOR_CAFE

    pf1 = cf1.paragraphs[0]
    pf1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rf1 = pf1.add_run("RECIBÍ FINIQUITO A MI ENTERA SATISFACCIÓN\n\n\n\n___________________________________\nC. ________________________________\nNombre, Firma y Fecha")
    rf1.font.name = 'Segoe UI'
    rf1.font.size = Pt(8)
    rf1.font.bold = True
    rf1.font.color.rgb = COLOR_CAFE

    set_cell_border(cf2, top={'val':'single','sz':4,'color':'535839'}, bottom={'val':'single','sz':4,'color':'535839'}, left={'val':'single','sz':4,'color':'535839'}, right={'val':'single','sz':4,'color':'535839'})
    pf2 = cf2.paragraphs[0]
    pf2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rf2 = pf2.add_run("\n\n\n\nHUELLA DIGITAL\nPulgar Derecho")
    rf2.font.name = 'Segoe UI'
    rf2.font.size = Pt(7)
    rf2.font.color.rgb = COLOR_MUTED

    return doc


# ==============================================================================
# 6. GENERACIÓN DEL CHECKLIST EN TXT CON ✅ Y ❌ Y GUARDADO SINCRONIZADO
# ==============================================================================
CHECKLIST_TXT_CONTENT = """================================================================================
🧁 BAKE ME UP - CHECKLIST ACTUALIZADO DE EXPEDIENTES DE PERSONAL (OCTUBRE 2026)
================================================================================
Titular: Ing. Sofía Gavito Alarcón | Sucursal: Plaza Pabellón Las Torres

RESUMEN DEL EQUIPO ACTIVO (5 COLABORADORES):
1. José Del Castillo Olvera (José)     - Tiempo Completo (5 días) - $9,500/mes
2. Areli Daniela Ortiz Sánchez (Dani)  - Tiempo Completo (6 días) - $9,500/mes
3. María Itzel Alanís Castro (Itzel)   - Medio Tiempo (6 días)    - $7,000/mes
4. Paulina Mejía Jiménez (Pau)         - Medio Tiempo (6 días)    - $4,500/mes
5. Ivonne [Apellidos Pendientes]       - Medio Tiempo (6 días)    - $4,000/mes


================================================================================
 DETALLE DE DOCUMENTOS POR COLABORADOR ( ✅ = En Carpeta | ❌ = Falta Pedir )
================================================================================

--------------------------------------------------------------------------------
1. JOSÉ DEL CASTILLO OLVERA (Encargado de Producción | CURP: OECJ020724HPLLSSA4)
--------------------------------------------------------------------------------
  ✅ Contrato Individual de Trabajo Firmado (Contrato Laboral Firmado - Jose Del Castillo Olvera.pdf)
  ✅ Reglamento Interno de Trabajo Firmado (Reglamento Jose.pdf)
  ✅ Carta de Ascenso e Incremento Salarial Firmada (Aumento Jose.pdf - $9,500.00 MXN)
  ✅ Identificación Oficial INE (INSTITUTO NACIONAL ELECTORAL 5.pdf)
  ✅ CURP Oficial (CURP_OECJ020724HPLLSSA4 (1).pdf)
  ✅ Constancia de Manejo Higiénico de Alimentos (Curso Manejo de Alimentos.pdf)
  ❌ Acta de Nacimiento Propia (OJO: El archivo actual en su carpeta es el acta de su hijo)
  ❌ Comprobante de Domicilio Reciente (Agua o CFE no mayor a 3 meses)
  ❌ Constancia de Situación Fiscal (CSF SAT)

--------------------------------------------------------------------------------
2. ARELI DANIELA ORTIZ SÁNCHEZ (Producción | CURP: OISA020209MBCRNRA0)
--------------------------------------------------------------------------------
  ✅ Contrato Individual de Trabajo Firmado (Contrato dani.pdf)
  ❌ Reglamento Interno de Trabajo Firmado (PRIORIDAD ALTA: Imprimir hoja 17 del RIT y que la firme)
  ✅ Identificación Oficial INE (INE Areli Daniela Ortiz Sanchez.pdf)
  ✅ CURP Oficial (curp-2.pdf)
  ✅ Acta de Nacimiento (ACTA DE NACIMIENTO Areli Daniela.pdf)
  ✅ Constancia de Manejo Higiénico de Alimentos (CONSTANCIA MANEJO DE ALIMENTOS.pdf)
  ❌ Comprobante de Domicilio Reciente
  ❌ Constancia de Situación Fiscal (CSF SAT)

--------------------------------------------------------------------------------
3. PAULINA MEJÍA JIMÉNEZ (Barra y Bebidas | CURP: MEJP040112MPLJMLA1)
--------------------------------------------------------------------------------
  ❌ Contrato Individual de Trabajo Firmado (PRIORIDAD URGENTE: No tiene contrato firmado en carpeta)
  ✅ Reglamento Interno de Trabajo Firmado (Reglamento Interno Firmado - Paulina Mejia.pdf)
  ✅ Carta Compromiso Operativo Firmada (BakeMeUp_Carta_Compromiso_Operativo_Paulina_Mejia_14_Octubre_2026_Firmada.pdf)
  ✅ Identificación Oficial INE (Ine Pau.pdf)
  ✅ CURP Oficial (CURP.pdf)
  ✅ Acta de Nacimiento (ACTA DE NACIMIENTO.heic)
  ✅ Comprobante de Domicilio (COMPROBANTE DE DOMICILIO.pdf)
  ✅ Constancia de Manejo Higiénico de Alimentos (CONSTANCIA MANEJO DE ALIMENTOS.pdf)
  ❌ Constancia de Situación Fiscal (CSF SAT)

--------------------------------------------------------------------------------
4. MARÍA ITZEL ALANÍS CASTRO (Producción y Vitrina | CURP: AACI020912MPLLSTA0)
--------------------------------------------------------------------------------
  ❌ Contrato Individual de Trabajo Firmado (PRIORIDAD URGENTE: No tiene contrato firmado en carpeta)
  ✅ Reglamento Interno de Trabajo Firmado (Reglamento Interno Firmado - Maria Itzel Alanis.pdf)
  ✅ Carta Compromiso Operativo Firmada (BakeMeUp_Carta_Compromiso_Operativo_Itzel_Alanis_14_Octubre_2026_Firmada.pdf)
  ✅ Identificación Oficial INE (Identificacion Oficial INE - Maria Itzel Alanis.pdf)
  ❌ CURP Oficial
  ❌ Acta de Nacimiento
  ❌ Comprobante de Domicilio Reciente
  ❌ Constancia de Manejo Higiénico de Alimentos
  ❌ Constancia de Situación Fiscal (CSF SAT)

--------------------------------------------------------------------------------
5. IVONNE [APELLIDOS Y CURP PENDIENTES] (Medio Tiempo - Limpieza y Apoyo)
--------------------------------------------------------------------------------
  ❌ Contrato Individual de Trabajo Firmado (PRIORIDAD URGENTE)
  ❌ Reglamento Interno de Trabajo Firmado (PRIORIDAD URGENTE)
  ❌ Identificación Oficial INE (Por ambos lados)
  ❌ CURP Oficial
  ❌ Acta de Nacimiento
  ❌ Comprobante de Domicilio Reciente
  ❌ Constancia de Manejo Higiénico de Alimentos
  ❌ Constancia de Situación Fiscal (CSF SAT)


================================================================================
 HISTÓRICO DE BAJAS (Movidas a carpeta '00_Bajas_Historico')
================================================================================
• ALEJANDRA HERNÁNDEZ DE JESÚS (CURP: HEJA051104MPLRSLA5) - BAJA:
  ✅ Contrato Laboral Firmado
  ✅ Reglamento Interno Firmado
  ✅ Identificación Oficial INE
  ❌ Carta de Renuncia Voluntaria y Finiquito Firmado


================================================================================
 PLAN RÁPIDO DE REGULARIZACIÓN PARA ESTA SEMANA (3 ACCIONES CLAVE)
================================================================================
1. CONTRATOS FALTANTES: Imprimir y firmar el '01_Formato_Contrato_Individual_Trabajo_BakeMeUp_Maestro.docx'
   con PAULINA, ITZEL e IVONNE (con huella digital en cada hoja).
2. REGLAMENTOS FALTANTES: Hacer que DANI e IVONNE firmen la hoja de conformidad del
   Reglamento Interior de Trabajo y escanearla en sus carpetas.
3. BLINDAJE CADA QUINCENA: Al pagar cada día 15 y 30, imprimir una hoja del
   '02_Formato_Recibo_Quincenal_Nomina_y_Propinas_BakeMeUp.docx' y recabar su firma.
================================================================================
"""

def main():
    os.makedirs('docs', exist_ok=True)

    # Resolver ruta de BAKE ME UP ADMINISTRACION
    base = r"G:\.shortcut-targets-by-id\1b2fZ7hp348TbKpb46Y0jqZqoWvkfxHYi\BAKE ME UP ADMINISTRACION"
    admin_dir = [os.path.join(base, d) for d in os.listdir(base) if 'admin' in d.lower()][0]
    rh_dir = [os.path.join(admin_dir, d) for d in os.listdir(admin_dir) if 'recurs' in d.lower()][0]
    plantillas_dir = [os.path.join(rh_dir, d) for d in os.listdir(rh_dir) if 'plantilla' in d.lower()][0]

    # 1. Guardar el Checklist TXT con UTF-8-SIG (para que Bloc de Notas de Windows muestre ✅ y ❌ perfecto)
    chk_drive_1 = os.path.join(rh_dir, "CHECKLIST_ESTADO_ACTUAL_EXPEDIENTES_BMU.txt")
    chk_drive_2 = os.path.join(rh_dir, "README Checklist Expediente de Personal.txt")
    chk_local = os.path.abspath(os.path.join("docs", "CHECKLIST_ESTADO_ACTUAL_EXPEDIENTES_BMU.txt"))

    for path_txt in (chk_drive_1, chk_drive_2, chk_local):
        with open(path_txt, "w", encoding="utf-8-sig") as f:
            f.write(CHECKLIST_TXT_CONTENT)
        print("Checklist guardado en:", path_txt)

    # 2. Construir y guardar los 5 formatos maestros .docx
    docs_to_build = [
        ("01_Formato_Contrato_Individual_Trabajo_BakeMeUp_Maestro.docx", build_contrato_maestro),
        ("02_Formato_Recibo_Quincenal_Nomina_y_Propinas_BakeMeUp.docx", build_recibo_quincenal),
        ("03_Formato_Bitacora_Quincenal_Asistencia_BakeMeUp.docx", build_bitacora_asistencia),
        ("04_Formato_Acta_Administrativa_Oficial_BakeMeUp.docx", build_acta_administrativa),
        ("05_Formato_Renuncia_Voluntaria_y_Finiquito_BakeMeUp.docx", build_renuncia_y_finiquito),
    ]

    for filename, builder_fn in docs_to_build:
        doc_obj = builder_fn()
        local_p = os.path.abspath(os.path.join("docs", filename))
        drive_p = os.path.join(plantillas_dir, filename)
        doc_obj.save(local_p)
        doc_obj.save(drive_p)
        print(f"Generado y sincronizado: {filename}")

if __name__ == "__main__":
    main()
