from reportlab.pdfgen import canvas
from jgp_report_creditos.core.exception.exception import ContratoError
from jgp_utils.utils import Utils
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Spacer, Paragraph, Table, PageBreak)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
import datetime
import os.path

#Add styles
estilos = getSampleStyleSheet()
#type of styles
tamanio_letra = 8.5
estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontSize=tamanio_letra, fontName = 'Helvetica'))
estilos.add(ParagraphStyle(name='left', alignment=TA_LEFT, fontSize=tamanio_letra, fontName = 'Helvetica'))
estilos.add(ParagraphStyle(name='center', alignment=TA_CENTER, fontSize=tamanio_letra, fontName = 'Helvetica'))
estilos.add(ParagraphStyle(name = 'Inciso', alignment=TA_JUSTIFY, bulletAnchor = 'start', fontSize=tamanio_letra, fontName = 'Helvetica'))
estilos.add(ParagraphStyle(name = 'Terror', alignment=TA_CENTER, fontSize=40, textColor= 'red', fontName = 'Helvetica'))
estilos.add(ParagraphStyle(name = 'Derror', alignment=TA_CENTER, fontSize=12, textColor= 'black', fontName = 'Helvetica'))

# Margenes del documento
def documentos(nombre_document):
    return SimpleDocTemplate(nombre_document, pagesize=letter, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=24*mm, bottomMargin=17*mm)

class NumberedCanvas(canvas.Canvas):
    """
        Crea el pie de pagina para que muestre en las hojas del documento
        Args:
            - canvas.Canvas: Requiere un canva.
            
    """
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.Canvas = canvas.Canvas
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        # escribe el pie de pagina
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            self.Canvas.showPage(self)
        self.Canvas.save(self)
    def draw_page_number(self, page_count):  
        self.setFont('Helvetica',8)
        x,y= letter
        page = " %s de %s" % (self._pageNumber, page_count)       
        self.saveState()
        self.drawString(x/2, 1*cm, page) # Agregar footer en cada página "creo el pie de pagina (x de y)"
        self.restoreState()

# -------------------------- PARRAFOS DE LOS CONTRATOS ------------------------------
class BaseContrato :   
    _parrafos = []
    # crea constructores
    def __init__(self, contrato, usuario):
        self.__contrato = contrato
        self.usuario = usuario # usuario que se loguea enviado por Lic.
    # footer and header
    def _encabezado(self,canvas,doc):
        """
        Crea el encabezado estatico de las paginas del documento y asi tambien la imagen para las paginas impares 
        Args:
            - canvas (canvas): Un canvas.
            - doc (documento): Un SimpleDocTemplate
            - self           : Un json (diccionario) y un usuario (string)
        """
        # Encabezado de pagina 
        canvas.saveState()
        canvas.setFont('Helvetica',5.8) # tipo y tamaño de letra
        x= datetime.datetime.now() # obtengo la fecha actual
        formatoFecha= x.strftime("%d/%m/%Y") # setting model of date
        codigo_operacion=self.__contrato["codigo_operacion"]
        #posicion del encabezado(x, y, texto)
        canvas.drawString(2*cm, A4[1]-86, formatoFecha)
        canvas.drawString(2*cm, A4[1]-94, str(self.usuario))
        canvas.drawString(2*cm, A4[1]-103, codigo_operacion)
        canvas.restoreState()
        # Añado imagen a las paginas impares
        canvas.saveState()
        canvas.setFont('Helvetica',7)
        if(doc.page%2!=0):# dibuja a paginas impares
            img = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../../resources/img/logo_jgp.png')# Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
            canvas.drawImage(img, 14*cm, 730, 160, 35, mask=None)     
        canvas.restoreState()

    # pdf en blanco ERROR
    def _error_mensaje(self, title_error, description_error):
        """
        Si ocurre una exception, elimina toda la informacion que haya en self._parrafos = []
        Args:
            - self  : Un json (diccionario) y un usuario (string)
            - title_error (string): Un string que contiene el titulo del error.
            - description_error (string): Un string que da la descripcion del error
        """
        self._parrafos.clear()
        titulo=f'<b>{title_error}</b> <br/> '
        self._parrafos.append(Paragraph(titulo, estilos["Terror"]))
        self._parrafos.append(Paragraph("________________", estilos["Terror"]))
        texto = f'  <br/>\
                    <br/>\
                    <br/>\
                    <br/>\
                        '  
        self._parrafos.append(Paragraph(texto, estilos["Terror"]))
        texto = f'<b>"{description_error}"</b>'        
        self._parrafos.append(Paragraph(texto, estilos["Derror"]))

    #Para todos los contratos
    def _tipo_contrato(self, tipo_concepto):
        """
        Añade la primera parte del contrato en donde especifica el tipo de contrato que es
        Args:
            - tipo_concepto (String): Es un String el cual especifica el tipo de contrato
            - self  : Un json (diccionario) y un usuario (string)
        """
        titulo='<b >DOCUMENTO PRIVADO</b> <br/>'
        self._parrafos.append(Paragraph(titulo, estilos["center"]))
        texto = f'Conste por el presente documento privado de un contrato de <b>{tipo_concepto}</b>, que \
            previo reconocimiento de firmas y rúbricas ante autoridad competente, podrá \
            ser elevada a la categoría de instrumento público, de acuerdo al Artículo 1297 del Código Civil, suscrito \
            al tenor y contenido de las siguientes cláusulas:'        
        self._parrafos.append(Paragraph(texto, estilos["Justify"]))
    
    def _partes_contratantes(self, numeral):
        """
        Esta funcion añade: PARTES CONTRATANTES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: si no tiene fiadores
        """
        # Obtengo los datos del testimonio real
        testimonio_poder=self.__contrato["testimonio_poder"]       
        domicilio_legal = testimonio_poder["sucursal"]["direccion"]
        apoderado = self.nombreCompleto_repre()
        numero_ci_apoderado = testimonio_poder["representante_legal"]["ci"]
        cargo = testimonio_poder["representante_legal"]["rol"]       
        numero_testimonio = testimonio_poder["numero_testimonio"]
        fecha_testimonio = Utils.get_fecha(self, testimonio_poder["fecha_testimonio"])
        numero_notaria = testimonio_poder["numero_notaria_publica"]
        responsable_notaria = testimonio_poder["nombre_notario_publico"]
        texto = f'<b><u>{numeral}</u>.- (PARTES CONTRATANTES)</b>.- Intervienen en la suscripción del presente contrato:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = f'<b>GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A.</b>, sociedad \
            legalmente constituida bajo las leyes del Estado Plurinacional de Bolivia, con Matrícula de \
            Comercio y Número de Identificación Tributaria 173788022, con domicilio en la \
            {domicilio_legal} de esta ciudad, representada legalmente por <b>{apoderado}</b>, con C.I. Nº {numero_ci_apoderado}, mayor de edad, hábil \
            por derecho y vecino(a) de esta ciudad, en su condición de {cargo} en mérito al \
            Testimonio Poder No. {numero_testimonio} de fecha {fecha_testimonio} otorgado por ante la \
            Notaría de Fe Pública Nº {numero_notaria} del Distrito Judicial de La Paz a cargo de(la) Dr(a).\
            {responsable_notaria}, quien en adelante se denominará <b>"EL ACREEDOR"</b>.'
        b = "El(la)(los) señor(a)(es) "
        deudores = self.get_deudores()
        i=0
        for item in deudores:
            i+=1
            nombreDeudor = item['nombre_completo'].upper()
            numeroCiDeudor = item['ci']
            estadoCivilDeudor = self.get_estado_civil(item['estado_civil'],item['genero'])
            domicilioDeudor = item['direccion']
            domicilio_deudor = self.get_articulo_direccion(domicilioDeudor)
            aux = f'<b>{nombreDeudor}</b> con <b>C.I. Nº {numeroCiDeudor}</b>, de nacionalidad \
                boliviana, de estado civil {estadoCivilDeudor}, domiciliado(a)(s) en {domicilio_deudor}'
            b = b + aux
            if (i != len(deudores)-1):          
                b = b + ","+" "
            else:
                b = b + " y"+" "
        aux1='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        b=b+aux1
        #para el inciso c
        fiadores = self.get_fiadores()
        if(len(fiadores)>0):
            c=""
            c = "El(la)(los) señor(a)(es) "
            j=0
            for item in fiadores:
                j+=1
                nombreFiador = item['nombre_completo'].upper()
                numeroCiFiador = item['ci']
                estadoCivilFiador = self.get_estado_civil(item['estado_civil'],item['genero'])
                domicilioFiador = item['direccion']
                domicilio_fiador = self.get_articulo_direccion(domicilioFiador)
                auxfiador = f'<b>{nombreFiador}</b> con <b>C.I. Nº {numeroCiFiador}</b>, de nacionalidad \
                boliviana, de estado civil {estadoCivilFiador}, domiciliado(a)(s) en {domicilio_fiador}'
                c = c + auxfiador
                if (j != len(fiadores)-1):
                    c = c + ","+" "
                else:
                    c = c + " y"+" "
            aux3='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>.'
            c=c+aux3        
            incisos = ListFlowable(
            [
                Paragraph(a, estilos['Inciso']),
                Paragraph(b, estilos['Inciso']),                      
                Paragraph(c, estilos['Inciso']),     
            ],            
            bulletType='a',
            bulletFormat='%s)',
            leftIndent=40,
            bulletColor='black',
            bulletFontName='Helvetica-Bold',
            bulletFontSize=tamanio_letra,
            bulletOffsetY=0,
            bulletDedent=20        
            )
            self._parrafos.append(incisos)
        else:   
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de fiadores")
    
    #12
    def _partes_contratantes3(self, numeral):
        """
        Esta funcion añade: PARTES CONTRATANTES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: si no tiene garantes
        """
        # Testimonio real
        testimonio_poder=self.__contrato["testimonio_poder"]       
        domicilio_legal = testimonio_poder["sucursal"]["direccion"]
        apoderado = self.nombreCompleto_repre()
        numero_ci_apoderado = testimonio_poder["representante_legal"]["ci"]
        cargo = testimonio_poder["representante_legal"]["rol"]       
        numero_testimonio = testimonio_poder["numero_testimonio"]
        fecha_testimonio = Utils.get_fecha(self, testimonio_poder["fecha_testimonio"])
        numero_notaria = testimonio_poder["numero_notaria_publica"]
        responsable_notaria = testimonio_poder["nombre_notario_publico"]
        texto = f'<b><u>{numeral}</u>.- (PARTES CONTRATANTES)</b>.- Intervienen en la suscripción del presente contrato:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = f'<b>GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A.</b>, sociedad \
            legalmente constituida bajo las leyes del Estado Plurinacional de Bolivia, con Matrícula de \
            Comercio y Número de Identificación Tributaria 173788022, con domicilio en la \
            {domicilio_legal} de esta ciudad, representada legalmente por <b>{apoderado}</b>, con C.I. Nº {numero_ci_apoderado}, mayor de edad, hábil \
            por derecho y vecino(a) de esta ciudad, en su condición de {cargo} en mérito al \
            Testimonio Poder No. {numero_testimonio} de fecha {fecha_testimonio} otorgado por ante la \
            Notaría de Fe Pública Nº {numero_notaria} del Distrito Judicial de La Paz a cargo de(la) Dr(a).\
            {responsable_notaria}, quien en adelante se denominará <b>"EL ACREEDOR"</b>.'
        # Insiso b)
        b = "El(la)(los) señor(a)(es) "
        deudores = self.get_deudores()
        i=0
        for item in deudores:
            i+=1
            nombreDeudor = item['nombre_completo'].upper()
            numeroCiDeudor = item['ci']
            estadoCivilDeudor = self.get_estado_civil(item['estado_civil'],item['genero'])
            domicilioDeudor = item['direccion']
            domicilio_deudor = self.get_articulo_direccion(domicilioDeudor)
            aux = f'<b>{nombreDeudor}</b> con <b>C.I. Nº {numeroCiDeudor}</b>, de nacionalidad \
                boliviana, de estado civil {estadoCivilDeudor}, domiciliado(a)(s) en {domicilio_deudor}'
            b = b + aux
            if (i != len(deudores)-1):
                b = b + ","+" "
            else:
                b = b + " y"+" "
        aux1='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        b=b+aux1
        # Insiso c)
        fiadores = self.get_fiadores()
        c=""
        if(len(fiadores)>0):
            c = "El(la)(los) señor(a)(es) "
            j=0
            for item in fiadores:
                j+=1
                nombreFiador = item['nombre_completo'].upper()
                numeroCiFiador = item['ci']
                estadoCivilFiador = self.get_estado_civil(item['estado_civil'],item['genero'])
                domicilioFiador = item['direccion']
                domicilio_fiador = self.get_articulo_direccion(domicilioFiador)
                auxfiador = f'<b>{nombreFiador}</b> con <b>C.I. Nº {numeroCiFiador}</b>, de nacionalidad \
                boliviana, de estado civil {estadoCivilFiador}, domiciliado(a)(s) en {domicilio_fiador}'
                c = c + auxfiador
                if (j != len(fiadores)-1):
                    c = c + ","+" "
                else:
                    c = c + " y"+" "
            aux3='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) DEPOSITARIO(S) y/o GARANTE(S) PERSONAL(ES)"</b>.'
            c=c+aux3        
            incisos = ListFlowable(
            [
                Paragraph(a, estilos['Inciso']),
                Paragraph(b, estilos['Inciso']),                      
                Paragraph(c, estilos['Inciso']),     
            ],            
            bulletType='a',
            bulletFormat='%s)',
            leftIndent=40,
            bulletColor='black',
            bulletFontName='Helvetica-Bold',
            bulletFontSize=tamanio_letra,
            bulletOffsetY=0,
            bulletDedent=20        
            )
            self._parrafos.append(incisos)
        else:   
            raise ContratoError("Campo requerido", "El contrato requiere los Datos del(los) Garante(es)")
    
    def _partes_contratantes2(self, numeral):
        """
        Esta funcion añade: PARTES CONTRATANTES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: 
            - si no tiene fiadores
            - si envia en tipo de garantia Quirografaria a un garante
        """
        # Testimonio real
        testimonio_poder=self.__contrato["testimonio_poder"]       
        domicilio_legal = testimonio_poder["sucursal"]["direccion"]
        apoderado = self.nombreCompleto_repre()
        numero_ci_apoderado = testimonio_poder["representante_legal"]["ci"]
        cargo = testimonio_poder["representante_legal"]["rol"]       
        numero_testimonio = testimonio_poder["numero_testimonio"]
        fecha_testimonio = Utils.get_fecha(self, testimonio_poder["fecha_testimonio"])
        numero_notaria = testimonio_poder["numero_notaria_publica"]
        responsable_notaria = testimonio_poder["nombre_notario_publico"]
        texto = f'<b><u>{numeral}</u>.- (PARTES CONTRATANTES)</b>.- Intervienen en la suscripción del presente contrato:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = f'<b>GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A.</b>, sociedad \
            legalmente constituida bajo las leyes del Estado Plurinacional de Bolivia, con Matrícula de \
            Comercio y Número de Identificación Tributaria 173788022, con domicilio en la \
            {domicilio_legal} de esta ciudad, representada legalmente por <b>{apoderado}</b>, con C.I. Nº {numero_ci_apoderado}, mayor de edad, hábil \
            por derecho y vecino(a) de esta ciudad, en su condición de {cargo} en mérito al \
            Testimonio Poder No. {numero_testimonio} de fecha {fecha_testimonio} otorgado por ante la \
            Notaría de Fe Pública Nº {numero_notaria} del Distrito Judicial de La Paz a cargo de(la) Dr(a).\
            {responsable_notaria}, quien en adelante se denominará <b>"EL ACREEDOR"</b>.'      
        b = "El(la)(los) señor(a)(es)"
        deudores = self.get_deudores()
        if(len(deudores)>0):
            i=0
            for item in deudores:
                i+=1
                nombre_deudor = item['nombre_completo'].upper()
                numeroCiDeudor = item['ci']
                estadoCivilDeudor = self.get_estado_civil(item['estado_civil'],item['genero'])
                domicilioDeudor = item['direccion']
                domicilio_deudor = self.get_articulo_direccion(domicilioDeudor)
                aux = f'<b> {nombre_deudor} </b> con <b>C.I. Nº {numeroCiDeudor}</b>, de nacionalidad \
                    boliviana, de estado civil {estadoCivilDeudor}, domiciliado(a)(s) en {domicilio_deudor}'
                b = b + aux
                if (i != len(deudores)-1):
                    b = b + ","+" "
                else:
                    b = b + " y"+" "       
            aux1='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
            b=b+aux1
            incisos = ListFlowable(
            [
                Paragraph(a, estilos['Inciso']),
                Paragraph(b, estilos['Inciso']),                          
            ],            
            bulletType='a',
            bulletFormat='%s)',
            leftIndent=40,
            bulletColor='black',
            bulletFontName='Helvetica-Bold',
            bulletFontSize=tamanio_letra,
            bulletOffsetY=0,
            bulletDedent=20        
            )
            self._parrafos.append(incisos)
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Fiadores")

        fiadores = self.get_fiadores()
        tipo_garantia=self.__contrato["tipo_garantia"]["descripcion"]
        if(len(fiadores)>0 and tipo_garantia=="Quirografaria"):
            raise ContratoError("Datos erroneos", "Este tipo de contrato no admite garantes y/o garantias")
        if(len(fiadores)>0):
            raise ContratoError("Datos erroneos", "Este tipo de contrato no admite garantes")
        
    def _partes_contratantes2Soli(self, numeral):
        """
        Esta funcion añade: PARTES CONTRATANTES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: si no tiene 3 fiadores minimamente
        """
        #TESTIMONIO REAL
        testimonio_poder=self.__contrato["testimonio_poder"]       
        domicilio_legal = testimonio_poder["sucursal"]["direccion"]
        apoderado = self.nombreCompleto_repre()
        numero_ci_apoderado = testimonio_poder["representante_legal"]["ci"]
        cargo = testimonio_poder["representante_legal"]["rol"]       
        numero_testimonio = testimonio_poder["numero_testimonio"]
        fecha_testimonio = Utils.get_fecha(self, testimonio_poder["fecha_testimonio"])
        numero_notaria = testimonio_poder["numero_notaria_publica"]
        responsable_notaria = testimonio_poder["nombre_notario_publico"]
        texto = f'<b><u>{numeral}</u>.- (PARTES CONTRATANTES)</b>.- Intervienen en la suscripción del presente contrato:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = f'<b>GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A.</b>, sociedad \
            legalmente constituida bajo las leyes del Estado Plurinacional de Bolivia, con Matrícula de \
            Comercio y Número de Identificación Tributaria 173788022, con domicilio en la \
            {domicilio_legal} de esta ciudad, representada legalmente por <b>{apoderado}</b>, con C.I. Nº {numero_ci_apoderado}, mayor de edad, hábil \
            por derecho y vecino(a) de esta ciudad, en su condición de {cargo} en mérito al \
            Testimonio Poder No. {numero_testimonio} de fecha {fecha_testimonio} otorgado por ante la \
            Notaría de Fe Pública Nº {numero_notaria} del Distrito Judicial de La Paz a cargo de(la) Dr(a).\
            {responsable_notaria}, quien en adelante se denominará <b>"EL ACREEDOR"</b>.'      
        b = "El(la)(los) señor(a)(es)"
        deudores = self.get_deudores()
        if(len(deudores)>2):
            i=0
            for item in deudores:
                i+=1
                nombre_deudor = item['nombre_completo'].upper()
                numeroCiDeudor = item['ci']
                estadoCivilDeudor = self.get_estado_civil(item['estado_civil'],item['genero'])
                domicilioDeudor = item['direccion']
                domicilio_deudor = self.get_articulo_direccion(domicilioDeudor)
                aux = f'<b> {nombre_deudor} </b> con <b>C.I. Nº {numeroCiDeudor}</b>, de nacionalidad \
                    boliviana, de estado civil {estadoCivilDeudor}, domiciliado(a)(s) en {domicilio_deudor}'
                b = b + aux
                if (i != len(deudores)-1):
                    b = b + ","+" "
                else:
                    b = b + " y"+" "       
            aux1='mayor(es) de edad y hábil(es) por derecho, que en lo sucesivo se denominará(n) <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
            b=b+aux1
            incisos = ListFlowable(
            [
                Paragraph(a, estilos['Inciso']),
                Paragraph(b, estilos['Inciso']),                          
            ],            
            bulletType='a',
            bulletFormat='%s)',
            leftIndent=40,
            bulletColor='black',
            bulletFontName='Helvetica-Bold',
            bulletFontSize=tamanio_letra,
            bulletOffsetY=0,
            bulletDedent=20        
            )
            self._parrafos.append(incisos)
        else:
            raise ContratoError("Campo requerido", "Este tipo de garantia: Solidario, Requiere 3 deudores minimamente")
    
    def _objeto_del_contrato(self, numeral):
        """
        Esta funcion añade: OBJETO DEL CONTRATO, MONTO, MONEDA Y DESTINO DEL PRÉSTAMO, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        monto1=float(self.__contrato["monto_aprobado"])
        monto = Utils.literalEnteroMontoPrestamo(monto1)
        motivo_prestamo = self.__contrato["motivo_prestamo"].upper()
        texto_objeto = f'<b><u>{numeral}</u>.- (OBJETO DEL CONTRATO, MONTO, MONEDA Y DESTINO DEL PRÉSTAMO)</b>.- \
                        Mediante el presente contrato <b>"EL ACREEDOR"</b> otorga a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, un \
                        préstamo de dinero por la suma de <b>{monto}</b>; en moneda \
                        nacional que será utilizado exclusivamente para <b>{motivo_prestamo}</b>, \
                        conforme a disposiciones legales y reglamentarias vigentes, obligándose <b>"El(la)(los) DEUDOR(A)(ES)"</b> \
                        a pagar el mismo y las demás obligaciones emergentes o accesorios, en la forma y plazo estipulados en el presente contrato.'
        self._parrafos.append(Paragraph(texto_objeto, estilos['Justify']))
    
    def _desembolso(self, numeral):
        """
        Esta funcion añade: DESEMBOLSO, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_desembolso = f'<b><u>{numeral}</u>.- (DESEMBOLSO)</b>.- Gestión y Soporte de Proyectos Jesús del Gran Poder S.A. efectuará el \
                            desembolso del préstamo de dinero en la moneda pactada a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, \
                            mediante la boleta de desembolso y/o la orden de desembolso, cuya(s) constancia(s) formará(n) parte \
                            integrante e indivisible del presente contrato sin necesidad de ser transcrita(s).'
        self._parrafos.append(Paragraph(texto_desembolso, estilos['Justify']))
    
    def _gestion_cobranza(self, numeral):
        """
        Esta funcion añade: GESTIONES DE COBRANZA, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_gestion = f'<b><u>{numeral}</u>.- (GESTIONES DE COBRANZA)</b>.- Las partes acuerdan que los Gastos Operativos que \
        genere las Gestiones de Cobranza "in situ", serán cubiertas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o \
        <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>, éste acuerdo es pactado y autorizado de forma \
        voluntaria y expresa por <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>.'
        self._parrafos.append(Paragraph(texto_gestion, estilos['Justify']))

    def _gestion_cobranza3(self, numeral):
        """
        Esta funcion añade: GESTIONES DE COBRANZA, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_gestion = f'<b><u>{numeral}</u>.- (GESTIONES DE COBRANZA)</b>.- Las partes acuerdan que los Gastos Operativos que \
        genere las Gestiones de Cobranza "in situ", serán cubiertas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o \
        <b>"El(la)(los) GARANTE(S) PERSONAL(ES)"</b>, éste acuerdo es pactado y autorizado de forma \
        voluntaria y expresa por <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) GARANTE(S) PERSONAL(ES)"</b>.'
        self._parrafos.append(Paragraph(texto_gestion, estilos['Justify']))
    
    #CUARTA 2
    def _gestion_cobranza2(self, numeral):
        """
        Esta funcion añade: GESTIONES DE COBRANZA, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_gestion = f'<b><u>{numeral}</u>.- (GESTIONES DE COBRANZA)</b>.- Las partes acuerdan que los Gastos Operativos que \
        genere las Gestiones de Cobranza "in situ", serán cubiertas por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, éste \
        acuerdo es pactado y autorizado de forma voluntaria y expresa por <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        self._parrafos.append(Paragraph(texto_gestion, estilos['Justify']))
    
    def _intereses(self, numeral):
        """
        Esta funcion añade: INTERESES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        tasa_interes = self.__contrato["tasa_interes_mensual"]
        tasa_double=float(tasa_interes) # convertimos el string en double
        tasa_interes1 = Utils.literalDecimal(tasa_double).upper()
        texto_interes = f'<b><u>{numeral}</u>.- (INTERESES)</b>.- El préstamo objeto del presente contrato, devengará a favor de <b>"EL ACREEDOR"</b> \
                            los intereses descritos en el plan de pagos, documento que forma parte integrante e \
                            indivisible del presente contrato sin necesidad de ser transcrito, el cual contiene lo siguiente:'
        porcentaje = '% mensual'
        self._parrafos.append(Paragraph(texto_interes, estilos['Justify']))
        a = f'La tasa fija de interés aplicada al importe objeto del contrato será el equivalente al <b>{tasa_interes1}</b>\
            <b>POR CIENTO MENSUAL</b> (<b>{tasa_interes}</b><b>{porcentaje})</b>, la misma que será aplicada sobre el \
            saldo deudor de capital adeudado y calculado hasta la fecha de pago. Dicha tasa no podrá ser \
            modificada o reajustada mientras el préstamo se encuentre vigente, teniendo <b>"El(la)(los) DEUDOR(A)(ES)"</b>\
            la opción de pagar anticipadamente su obligación si así lo desea(n), de conformidad al reglamento interno de pagos anticipados de la empresa.'       
        b = 'Del monto del préstamo concedido a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A. además de lo estipulado en el \
            punto anterior no cobrará comisiones o gastos que no hubiesen sido aceptados expresamente por escrito por <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        c = '<bullet></bullet> El cálculo de los saldos adeudados se encuentra previsto en el Plan de Pagos que \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> recibe(n) al momento de efectuarse el desembolso. Este cálculo consiste en restar el pago \
            del capital de la cuota al monto desembolsado o saldo anterior.'
        d = '<bullet></bullet> A tiempo de efectuarse el desembolso <b>"El(la)(los) DEUDOR(A)(ES)" y/o Fiador(a)(es)</b> tiene(n) la obligación de \
            recabar el Plan de Pagos correspondiente a la presente operación. '
        incisos = ListFlowable(
        [
            Paragraph(a,estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                      
            Paragraph(c, estilos['Inciso']),   
            Paragraph(d, estilos['Inciso']),            
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20
        )
        self._parrafos.append(incisos)
    
    #QUINTA 2
    def _intereses2(self, numeral):
        """
        Esta funcion añade: INTERESES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        tasa_interes = self.__contrato["tasa_interes_mensual"]
        #convertimos el string en double
        tasa_double=float(tasa_interes)
        tasa_interes1 = Utils.literalDecimal(tasa_double).upper()
        porcentaje = '% mensual'
        texto_interes = f'<b><u>{numeral}</u>.- (INTERESES)</b>.- El préstamo objeto del presente contrato, devengará a favor de <b>"EL ACREEDOR"</b> \
                            los intereses descritos en el plan de pagos, documento que forma parte integrante e \
                            indivisible del presente contrato sin necesidad de ser transcrito, el cual contiene lo siguiente:'
        self._parrafos.append(Paragraph(texto_interes, estilos['Justify']))
        a = f'La tasa fija de interés aplicada al importe objeto del contrato será el equivalente al <b>{tasa_interes1}</b> \
            <b>POR CIENTO MENSUAL</b> (<b>{tasa_interes}</b><b>{porcentaje})</b>, la misma que será aplicada sobre el \
            saldo deudor de capital adeudado y calculado hasta la fecha de pago. Dicha tasa no podrá ser \
            modificada o reajustada mientras el préstamo se encuentre vigente, teniendo <b>"El(la)(los) DEUDOR(A)(ES)"</b>\
            la opción de pagar anticipadamente su obligación si así lo desea(n), de conformidad al reglamento interno de pagos anticipados de la empresa.'
        b = 'Del monto del préstamo concedido a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A. además de lo estipulado en el \
            punto anterior no cobrará comisiones o gastos que no hubiesen sido aceptados expresamente por escrito por <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        c = 'El cálculo de los saldos adeudados se encuentra previsto en el Plan de Pagos que \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> recibe(n) al momento de efectuarse el desembolso. Este cálculo consiste en restar el pago \
            del capital de la cuota al monto desembolsado o saldo anterior.'
        d = ' A tiempo de efectuarse el desembolso <b>"El(la)(los) DEUDOR(A)(ES)"</b> tiene(n) la obligación de \
            recabar el Plan de Pagos correspondiente a la presente operación. '
        incisos = ListFlowable(
        [
            Paragraph(a, estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                      
            Paragraph(c, estilos['Inciso']), 
            Paragraph(d, estilos['Inciso']),     
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20        
        )
        self._parrafos.append(incisos)

    #contrato personal y vehiculo
    def _intereses_pyv(self, numeral):
        """
        Esta funcion añade: INTERESES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        tasa_interes = self.__contrato["tasa_interes_mensual"]
        tasa_double=float(tasa_interes) # convertimos el string en double
        tasa_interes1 = Utils.literalDecimal(tasa_double).upper()
        porcentaje = '% mensual'
        texto_interes = f'<b><u>{numeral}</u>.- (INTERESES)</b>.- El préstamo objeto del presente contrato, devengará a favor de <b>"EL ACREEDOR"</b> \
                            los intereses descritos en el plan de pagos, documento que forma parte integrante e \
                            indivisible del presente contrato sin necesidad de ser transcrito, el cual contiene lo siguiente:'
        self._parrafos.append(Paragraph(texto_interes, estilos['Justify']))
        a = f'La tasa fija de interés aplicada al importe objeto del contrato será el equivalente al <b>{tasa_interes1}</b> \
            <b>POR CIENTO MENSUAL</b> (<b>{tasa_interes}</b><b>{porcentaje})</b>, la misma que será aplicada sobre el \
            saldo deudor de capital adeudado y calculado hasta la fecha de pago. Dicha tasa no podrá ser \
            modificada o reajustada mientras el préstamo se encuentre vigente, teniendo <b>"El(la)(los) DEUDOR(A)(ES)"</b>\
            la opción de pagar anticipadamente su obligación si así lo desea(n), de conformidad al reglamento interno de pagos anticipados de la empresa.'
        b = 'Del monto del préstamo concedido a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A. además de lo estipulado en el \
            punto anterior no cobrará comisiones o gastos que no hubiesen sido aceptados expresamente por escrito por <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        c = 'El cálculo de los saldos adeudados se encuentra previsto en el Plan de Pagos que \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> recibe(n) al momento de efectuarse el desembolso. Este cálculo consiste en restar el pago \
            del capital de la cuota al monto desembolsado o saldo anterior.'
        d = ' A tiempo de efectuarse el desembolso <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o Garante(s) tiene(n) la obligación de \
            recabar el Plan de Pagos correspondiente a la presente operación. '
        incisos = ListFlowable(
        [
            Paragraph(a, estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                      
            Paragraph(c, estilos['Inciso']), 
            Paragraph(d, estilos['Inciso']),     
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20        
        )
        self._parrafos.append(incisos)

    def _intereses3(self, numeral):
        """
        Esta funcion añade: INTERESES, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        tasa_interes = self.__contrato["tasa_interes_mensual"]
        tasa_double=float(tasa_interes) # convertimos el string en double
        tasa_interes1 = Utils.literalDecimal(tasa_double).upper()
        texto_interes = f'<b><u>{numeral}</u>.- (INTERESES)</b>.- El préstamo objeto del presente contrato, devengará a favor de <b>"EL ACREEDOR"</b> \
                            los intereses descritos en el plan de pagos, documento que forma parte integrante e \
                            indivisible del presente contrato sin necesidad de ser transcrito, el cual contiene lo siguiente:'
        porcentaje = '% mensual'
        self._parrafos.append(Paragraph(texto_interes, estilos['Justify']))
        a = f'La tasa fija de interés aplicada al importe objeto del contrato será el equivalente al <b>{tasa_interes1}</b>\
            <b>POR CIENTO MENSUAL</b> (<b>{tasa_interes}</b><b>{porcentaje})</b>, la misma que será aplicada sobre el \
            saldo deudor de capital adeudado y calculado hasta la fecha de pago. Dicha tasa no podrá ser \
            modificada o reajustada mientras el préstamo se encuentre vigente, teniendo <b>"El(la)(los) DEUDOR(A)(ES)"</b>\
            la opción de pagar anticipadamente su obligación si así lo desea(n), de conformidad al reglamento interno de pagos anticipados de la empresa.'       
        b = 'Del monto del préstamo concedido a favor de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A. además de lo estipulado en el \
            punto anterior no cobrará comisiones o gastos que no hubiesen sido aceptados expresamente por escrito por <b>"El(la)(los) DEUDOR(A)(ES)"</b>.'
        c = '<bullet></bullet> El cálculo de los saldos adeudados se encuentra previsto en el Plan de Pagos que \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> recibe(n) al momento de efectuarse el desembolso. Este cálculo consiste en restar el pago \
            del capital de la cuota al monto desembolsado o saldo anterior.'
        d = '<bullet></bullet> A tiempo de efectuarse el desembolso <b>"El(la)(los) DEUDOR(A)(ES)" y/o GARANTE(S) PERSONAL(ES)</b> tiene(n) la obligación de \
            recabar el Plan de Pagos correspondiente a la presente operación. '
        incisos = ListFlowable(
        [
            Paragraph(a,estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                      
            Paragraph(c, estilos['Inciso']),   
            Paragraph(d, estilos['Inciso']),            
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20
        )
        self._parrafos.append(incisos)

    def getValoresDiccionarioFrecuencia(self, dict):
        """
        Esta funcion dado un diccionario busca la frecuencia del pago dado en el json y retorna su valor
        Args:
            - dict (dicccionario): Es un dicionario que le envian 
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            diccionario: Con el dato de la frecuencia
        Ayuda:
            list : devuelve una lista de las claves del diccionario
        """
        frecuencia=self.__contrato["frecuencia"]
        tiempo_numeral=self.__contrato["numero_cuotas"]
        if tiempo_numeral == 1:
            if(frecuencia=="Diario" or frecuencia=="Semanal" or frecuencia=="Catorcenal" or frecuencia=="28 dias" or frecuencia=="Mensual" or frecuencia=="Quincenal"): 
                llave=list(dict.keys())
                return  llave[llave.index(frecuencia)]
        else:
            if(frecuencia=="Diario" or frecuencia=="Semanal" or frecuencia=="Catorcenal" or frecuencia=="28 dias" or frecuencia=="Mensual" or frecuencia=="Quincenal"): 
                return  dict.get(frecuencia)
    
    #funcion retorna la frecuencia 
    def get_Frecuencia(self):
        """
        Esta funcion crea un diccionario y retorna su valor
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            diccionario: Con el dato de la frecuencia de DIAS, SEMANAS, .... etc.
        """
        dict = {"Diario": "DIAS","Semanal": "SEMANAS","Catorcenal": "CATORCENALES","28 dias": "MESES","Mensual": "MESES","Quincenal": "QUINCENAS"}
        return self.getValoresDiccionarioFrecuencia(dict)
    
    def get_Frecuencia2(self):
        """
        Esta funcion crea un diccionario y retorna su valor
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            diccionario: Con el dato de la frecuencia a pagos DIARIOS, SEMANALES,... etc.
        """
        dict = {"Diario": "DIARIOS","Semanal": "SEMANALES","Catorcenal": "CATORCENALES","28 dias": "MENSUALES","Mensual": "MENSUALES","Quincenal": "QUINCENALES"}
        return self.getValoresDiccionarioFrecuencia(dict)

    def _plazo(self, numeral):
        """
        Esta funcion añade: PLAZO, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        tiempo1=int(self.__contrato["numero_cuotas"])
        tiempo=Utils.literalNumeral(tiempo1)
        print("*********tiempo",tiempo)
        tiempo_numeral=self.__contrato["numero_cuotas"]
        #frecuencia = self.get_Frecuencia()

        if tiempo_numeral == 1:
            frecuencia1 = "("+str(tiempo_numeral)+")"+" "+"pago"+" "+self.get_Frecuencia2()
            computable="computable"
        else:
            frecuencia1 = "("+str(tiempo_numeral)+")"+" "+"pagos"+" "+self.get_Frecuencia2()
            computable="computables"
        print("frecuencia", frecuencia1)
        texto_plazo = f'<b><u>{numeral}</u>.- (PLAZO)</b>.- <b>"El(la)(los) DEUDOR(A)(ES)"</b> se compromete(n) a cumplir el presente contrato en un plazo de <b>{tiempo}</b> <b>{frecuencia1}</b>, {computable} a partir de la \
                        suscripción del presente contrato, obligándose <b>"El(la)(los) DEUDOR(A)(ES)"</b> a cancelar la totalidad de lo adeudado, a capital, \
                        intereses y reposición de gastos operativos y gestiones de cobranza, éste último si corresponde, de acuerdo al plan de pagos el cual es parte del presente \
                        documento sin necesidad de ser transcrito. Es responsabilidad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> conocer y tener una copia del plan de pagos que <b>"EL ACREEDOR"</b> \
                        emite al momento del desembolso, <b>"El(la)(los) DEUDOR(A)(ES)"</b> expresa(n) su conformidad y conocimiento del plan de pagos y \
                        condiciones de pago a la firma del presente contrato.'
        self._parrafos.append(Paragraph(texto_plazo, estilos['Justify']))
    
    def _lugar(self, numeral):
        """
        Esta funcion añade: LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES.., con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_lugar = f'<b><u>{numeral}</u>.- (LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES Y/O GASTOS, PENALIDAD)</b>.- Todos los pagos de la obligación contraída por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, \
                        capital, reposición de gastos operativos y gestiones de cobranza, intereses pactados y moratorios, deberán efectuarse en las oficinas de <b>"EL ACREEDOR"</b> y en moneda nacional, en \
                        las condiciones en que se produjo y convino el mismo y en la(s) fecha(s) de su(s) respectivo(s) vencimiento(s). Dichos pagos, ya sean dentro o fuera de juicio deberán ser efectuados \
                        en el monto indicado en las correspondientes liquidaciones de cada caso y a tal efecto elabore <b>"EL ACREEDOR"</b>, liquidaciones que en su caso serán actualizadas por la institución cuantas \
                        veces sea necesario, las mismas que harán fe en juicio. A simple requerimiento verbal o escrito de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>, \
                        <b>"EL ACREEDOR"</b> podrá diferir los intereses corrientes, moratorios y gastos operativos y gestiones de cobranza a las cuotas pendientes de pago.<br/>\
                        Adicionalmente y en caso de incumplimiento al plan de pagos, se cobrará y aplicará un interés legal equivalente al SEIS PUNTO CERO POR CIENTO ANUAL (6.0\u0025 anual) sobre el saldo insoluto.' 
        self._parrafos.append(Paragraph(texto_lugar, estilos['Justify']))      
    
    #12
    def _lugar_pyp(self, numeral):
        """
        Esta funcion añade: LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES.., con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_lugar = f'<b><u>{numeral}</u>.- (LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES Y/O GASTOS, PENALIDAD)</b>.- Todos los pagos de la obligación contraída por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, \
                        capital, reposición de gastos operativos y gestiones de cobranza, intereses pactados y moratorios, deberán efectuarse en las oficinas de <b>"EL ACREEDOR"</b> y en moneda nacional, en \
                        las condiciones en que se produjo y convino el mismo y en la(s) fecha(s) de su(s) respectivo(s) vencimiento(s). Dichos pagos, ya sean dentro o fuera de juicio deberán ser efectuados \
                        en el monto indicado en las correspondientes liquidaciones de cada caso y a tal efecto elabore <b>"EL ACREEDOR"</b>, liquidaciones que en su caso serán actualizadas por la institución cuantas \
                        veces sea necesario, las mismas que harán fe en juicio. A simple requerimiento verbal o escrito de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) GARANTE(S) PERSONAL(ES)"</b>, \
                        <b>"EL ACREEDOR"</b> podrá diferir los intereses corrientes, moratorios y gastos operativos y gestiones de cobranza a las cuotas pendientes de pago.<br/>\
                        Adicionalmente y en caso de incumplimiento al plan de pagos, se cobrará y aplicará un interés legal equivalente al SEIS PUNTO CERO POR CIENTO ANUAL (6.0\u0025 anual) sobre el saldo insoluto.' 
        self._parrafos.append(Paragraph(texto_lugar, estilos['Justify']))      
    
    #SÉPTIMA 2
    def _lugar2(self, numeral):
        """
        Esta funcion añade: LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES.., con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_lugar = f'<b><u>{numeral}</u>.- (LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES Y/O GASTOS, PENALIDAD)</b>.- Todos los pagos de la obligación contraída por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, \
            capital, reposición de gastos operativos y gestiones de cobranza, intereses pactados y moratorios, deberán efectuarse en las oficinas de <b>"EL ACREEDOR"</b> y en moneda nacional, en \
            las condiciones en que se produjo y convino el mismo y en la(s) fecha(s) de su(s) respectivo(s) vencimiento(s). Dichos pagos, ya sean dentro o fuera de juicio deberán ser efectuados \
            en el monto indicado en las correspondientes liquidaciones de cada caso y a tal efecto elabore <b>"EL ACREEDOR"</b>, liquidaciones que en su caso serán actualizadas por la institución cuantas \
            veces sea necesario, las mismas que harán fe en juicio. <br/>\
            A simple requerimiento verbal o escrito de <b>"El(la)(los) DEUDOR(A)(ES)"</b>, <b>"EL ACREEDOR"</b> podrá \
            diferir los intereses corrientes, moratorios y gastos operativos y gestiones de cobranza a las cuotas \
            pendientes de pago.'
        self._parrafos.append(Paragraph(texto_lugar, estilos['Justify']))              
        a = 'Adicionalmente y en caso de incumplimiento al plan de pagos, se cobrará y aplicará un interés legal equivalente al SEIS PUNTO CERO POR CIENTO ANUAL (6.0\u0025 anual) sobre el saldo insoluto.' 
        self._parrafos.append(Paragraph(a, estilos['Justify']))
    
    def _lugar_pyv(self, numeral):
        """
        Esta funcion añade: LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES.., con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_lugar = f'<b><u>{numeral}</u>.- (LUGAR, FORMA DE PAGO Y DIFERIMIENTO DE INTERESES Y/O GASTOS, PENALIDAD)</b>.- Todos los pagos de la obligación contraída por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, \
            capital, reposición de gastos operativos y gestiones de cobranza, intereses pactados y moratorios, deberán efectuarse en las oficinas de <b>"EL ACREEDOR"</b> y en moneda nacional, en \
            las condiciones en que se produjo y convino el mismo y en la(s) fecha(s) de su(s) respectivo(s) vencimiento(s). Dichos pagos, ya sean dentro o fuera de juicio deberán ser efectuados \
            en el monto indicado en las correspondientes liquidaciones de cada caso y a tal efecto elabore <b>"EL ACREEDOR"</b>, liquidaciones que en su caso serán actualizadas por la institución cuantas \
            veces sea necesario, las mismas que harán fe en juicio. <br/>\
            A simple requerimiento verbal o escrito de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o "<b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>", <b>"EL ACREEDOR"</b> podrá \
            diferir los intereses corrientes, moratorios y gastos operativos y gestiones de cobranza a las cuotas \
            pendientes de pago.'
        self._parrafos.append(Paragraph(texto_lugar, estilos['Justify']))              
        a = 'Adicionalmente y en caso de incumplimiento al plan de pagos, se cobrará y aplicará un interés legal equivalente al SEIS PUNTO CERO POR CIENTO ANUAL (6.0\u0025 anual) sobre el saldo insoluto.' 
        self._parrafos.append(Paragraph(a, estilos['Justify']))
    
    def _mora_ejecucion(self, numeral):
        """
        Esta funcion añade: MORA Y EJECUCIÓN, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto_mora = f'<b><u>{numeral}</u>.- (MORA Y EJECUCIÓN)</b>.- La demora o falta de pago total o parcial de la obligación ya sea de capital, intereses o accesorios, constituirá a <b>"El(la)(los) DEUDOR(A)(ES)"</b> \
        en mora automática por el total de la obligación, conforme al artículo 341 del Código Civil, la misma que se considera de plazo vencido, líquida y exigible sin necesidad de intimación o requerimiento \
        judicial o extrajudicial ni de otra formalidad o requisito, lo que da derecho a <b>"EL ACREEDOR"</b> para exigir el pago íntegro del saldo adeudado, intereses, accesorios, aunque el plazo final no se encuentre \
        vencido, pudiendo <b>"EL ACREEDOR"</b> ejercer la cobranza en forma pre judicial a través de su propio personal o por intermedio de servicios externos de cobranza, autorizándolo así de forma irretractable a \
        <b>"El(la)(los) DEUDOR(A)(ES)"</b> y demás obligados, quienes en caso de incumplimiento de sus obligaciones, reconocen a este título de préstamo suficiente fuerza ejecutiva por el importe consignado en la \
        liquidación emitida por la empresa. Dichas cobranzas podrán ser también ejercidas por la vía judicial, para lo cual <b>"EL ACREEDOR"</b> podrá interponer en cualquier momento la correspondiente acción para su cobranza \
        por la vía ejecutiva y otra vía judicial a elección de <b>"EL ACREEDOR"</b>, contra <b>"El(la)(los) DEUDOR(A)(ES)"</b> u otros obligados. Asimismo, se conviene que <b>"EL ACREEDOR"</b> a su elección podrá demandarlos en forma \
        individual o conjunta en la jurisdicción de la ciudad de La Paz - Bolivia, quedando en tal caso obligados, además al pago de todos los gastos, expensas, costos y costas ocasionados a <b>"EL ACREEDOR"</b> con la mora \
        de la obligación, incluyendo los emergentes de la cobranza judicial o extrajudicial, honorarios, derechos, costas y costos, sin excepción, todos los cuales serán pagados por <b>"El(la)(los) DEUDOR(A)(ES)"</b>, cualquiera \
        fuera el estado procesal a que llegue el juicio. \
        La espera o esperas que <b>"EL ACREEDOR"</b> acordare o permitiere no constituirá ni implicará prórroga del plazo señalado ni renovación del contrato, sino simples actos de liberalidad y tolerancia que en nada afectará ni \
        debilitará la fuerza ejecutiva de este contrato, ni los derechos de <b>"EL ACREEDOR"</b> para exigir judicialmente el pago del monto total del préstamo, accesorios, etc., en cualquier tiempo. Para el caso de llegar al \
        remate judicial de los bienes de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o los otros obligados, el remate se realizará sobre la base de los avalúos periciales efectuados por el valuador de <b>"EL ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto_mora, estilos['Justify']))

    def _caducidad_y_derecho_de_aceleracion(self, numeral):
        """
        Esta funcion añade: CADUCIDAD Y DERECHO DE ACELERACIÓN, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (CADUCIDAD Y DERECHO DE ACELERACIÓN)</b>.-  Independientemente de la mora de \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> por incumplimiento al plan de pagos pactado en este contrato, <b>"EL \
            ACREEDOR"</b> podrá unilateralmente acelerar el pago de todas las obligaciones asumidas por <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> y está autorizado a declarar la caducidad del plazo, por consiguiente suma \
            liquida y exigible y en mora de pleno derecho, bastando que <b>"EL ACREEDOR"</b> lo catalogue como \
            obligación vencida aunque el plazo o término de éstas no se encuentre vencido y, proceder a la \
            cobranza judicial del total de las obligaciones, intereses, accesorios, etc., sin necesidad de ninguna \
            intimación o requerimiento judicial o extrajudicial, por las siguientes causas: <b>1)</b> Incumplimiento de \
            cualquiera de las cláusulas o estipulaciones del presente contrato.- <b>2)</b> Si los bienes otorgados en \
            garantía son gravados con otras obligaciones, se desvalorizan o fueren perseguidos judicialmente o se \
            enajenan.- <b>3)</b> Disminución de la solvencia de <b>"El(la)(los) DEUDOR(A)(ES)"</b> a la sola apreciación y \
            criterio de <b>"EL ACREEDOR"</b>, o que se encuentren en mora, retrasados o con créditos castigados en \
            cualquier entidad financiera que los califiquen en categorías de mayor riesgo a los determinados por \
            <b>''EL ACREEDOR''.- 4)</b> Solicitud de concurso preventivo o de quiebra, o de concurso voluntario o \
            necesario.- <b>5)</b> Si la información proporcionada a <b>"EL ACREEDOR"</b> hubiera sido falsa, inexacta o \
            incorrectamente emitida.- <b>6)</b> Cuando se presenten cambios significativos adversos en el giro del \
            negocio o del sector económico en que se opera, a solo criterio de <b>"EL ACREEDOR".- 7)</b> Por \
            incumplimiento de sus obligaciones de pago en otros contratos celebrados con <b>"EL ACREEDOR".- 8)</b> \
            Falta de pago oportuno de cualquier cuota o amortización de cualquier obligación ya sea pago a capital, \
            intereses convenido y moratorio, aplicables de acuerdo al Plan de Pagos.- En general cualquier acto o \
            hecho de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o cualquier circunstancia que a criterio de <b>"EL ACREEDOR"</b> \
            pudiera poner en riesgo la total recuperación de las obligaciones contraídas por <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    def _garantias(self, numeral):  
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """     
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        texto_10_2 = "<b>10.2.</b> Con la Fianza personal, solidaria, mancomunada e indivisible del (la)(los) señor(a)(es)"
        fiadores = self.get_fiadores() # Obhtenemos a los fiadores
        i=0
        for item in fiadores:
            i+=1
            nombre_fiador = item['nombre_completo'].upper()
            numero_ci_fiador = item['ci']
            aux =f' <b>{nombre_fiador}</b> con <b>C.I. Nº</b> <b>{numero_ci_fiador}</b>'
            texto_10_2 = texto_10_2 + aux
            if (i != len(fiadores)-1):
                texto_10_2 = texto_10_2 +""
            else:
                texto_10_2 = texto_10_2 + " <b>y</b>"+" "
        aux1 =', cuyos datos generales se \
                encuentran especificadas en la cláusula primera del presente contrato, quien(es) se constituye(n) en \
                fiador(a)(es) de todas las obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> ante <b>"EL \
                ACREEDOR"</b>, y de todo lo estipulado en el presente contrato, y las inherentes y emergentes en forma \
                solidaria, mancomunada e indivisible con el(la) mismo(a) y entre sí, y en principal, liso(a) y llano(a) \
                pagador(a)(es) del préstamo, comisiones, intereses, impuestos, gastos, costas, etc., y demás cargos y \
                accesorios aplicables, renunciando de su parte a los beneficios de excusión, orden, división y otros \
                beneficios legales , aceptando para si todos los términos, comisiones y cláusulas estipuladas en el \
                presente contrato, obligándose al pago del préstamo y demás obligaciones en la misma condición y \
                calidad de obligado principal que <b>"El(la)(los) DEUDOR(A)(ES)"</b> y en forma incondicional e irrestricta.<br/> \
                Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
                obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa \
                extinguirá la garantía ni las obligaciones que <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> asume(n) \
                en tal calidad y como codeudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
                prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>. <b>"El(la)(los) \
                FIADOR(A)(ES) PERSONAL(ES)"</b> desde ya expresa(n) su acuerdo, consentimiento, sin que para \
                ello sea preciso ninguna comunicación ni aviso a <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> ni otra \
                formalidad o requisito, considerándose para todos los fines y efectos legales que dichas prórrogas, \
                renovaciones, etc., de producirse, son de conocimiento <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> \
                y cuenta con el acuerdo y consentimiento de éste(a).<br/>\
                <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> autoriza(n) que, \
                mediante una Fianza al contrato principal pueda mejorarse la garantía del préstamo solicitado sin \
                necesidad que la fianza este firmada por todos los integrantes del presente contrato.'
        texto_10_2=texto_10_2+aux1
        self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
    
    def _garantias_pyp(self, numeral):     
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene garantias reales por concepto de: Ubicacion ó Descripcion | ContratoError: Si no tiene garante(s)
        """
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        #10.2
        garantias=self.__contrato["garantias_reales"]
        if(len(garantias)>1):
            prendaria=self.detalleGarantia(self.get_prendaria())
            direccion_garantia=self.get_direccion_g()
            fiadores=self.get_fiadores()
            texto_10_2 = f' <b>10.2. "El(la)(los) DEUDOR(A)(ES)"</b> otorgará(n) al <b>ACREEDOR</b> como garantía {prendaria}, cuyas \
                características se encuentran detalladas y descritas en el formulario <b>"Avalúo de Garantía Prendaria"</b>, misma \
                que forma parte integrante de este contrato sin necesidad de ser transcrito, siendo aplicable para esta operación la \
                normativa legal vigente consignada en los artículos 1403 y siguientes del Código Civil.<br/> \
                A solicitud expresa del(la)(los) <b>DEPOSITARIO(S)</b> los bienes constituidos en prenda permanecerán en la <b>{direccion_garantia}</b>, bienes que quedarán en depósito y/o poder de '
            c=texto_10_2
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de la garantia real, revisar la garantia por concepto de: Ubicacion ó Descripcion")

        if(len(fiadores)>0):
            c = c+ '<b>"El(la)(los) GARANTE(S) DEPOSITARIO(S)"</b>'
            j=0
            for item in fiadores:
                j+=1
                nombreFiador = item['nombre_completo'].upper()
                numeroCiFiador = item['ci']
                auxfiador = f' <b>Sr(a). {nombreFiador}</b> con <b>C.I. Nº {numeroCiFiador}</b>'
                c = c + auxfiador
                if (j != len(fiadores)-1):
                    c = c + ","+" "
                else:
                    c = c + " y"+" "
            aux3='quien(es) a la suscripción del presente documento se declara(n) en posesión física, material y real de los bienes otorgados en prenda, los mismos que se encuentran en perfecto estado de conservación y/o funcionamiento, con las obligaciones y responsabilidades correspondientes al depositario gratuito, quedando encargado(s) de su cuidado, guarda y conservación por su cuenta exclusiva, asumiendo solidariamente todas las obligaciones y responsabilidades civiles y penales propias a su(s) condición(es) de depositario(s) que establecen disposiciones relativas al depósito y prenda, facultando a <b>"EL ACREEDOR"</b> a exigir su permanente exhibición, debiendo <b>"El(la)(los) DEPOSITARIO(S)"</b> mantener informado a <b>"EL ACREEDOR"</b> del lugar donde se encuentra la prenda, sobre cualquier cambio que se produzca respecto de la conservación o cualquier riesgo que puedan sufrir los bienes otorgados en prenda, dicha información debe realizarse por escrito dentro de los quinde (15) días siguientes de ocurrido el hecho. Trasladar la prenda a donde y cuando lo disponga <b>"EL ACREEDOR"</b>. Los bienes dados en prenda, no podrán ser cambiados del lugar de ubicación salvo consentimiento expreso de <b>"EL ACREEDOR".</b><br/> \
            Sobre los bienes de la prenda no existen obligaciones ni restricciones de ninguna clase que pudieran reclamar terceros, según declaración expresa que hace <b>"El(la)(los) DEUDOR(A)(ES)".</b>'
            self._parrafos.append(Paragraph(c+aux3, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de al menos un Garante")
        texto_10_3 = "<b>10.3.</b> Con la Garantía personal, solidaria, mancomunada e indivisible del (la)(los) señor(a)(es)"
        fiadores = self.get_fiadores() # Obhtenemos a los fiadores
        i=0
        for item in fiadores:
            i+=1
            nombre_fiador = item['nombre_completo'].upper()
            numero_ci_fiador = item['ci']
            aux =f' <b>{nombre_fiador}</b> con <b>C.I. Nº</b> <b>{numero_ci_fiador}</b>'
            texto_10_3 = texto_10_3 + aux
            if (i != len(fiadores)-1):
                texto_10_3 = texto_10_3 +""
            else:
                texto_10_3 = texto_10_3 + " <b>y</b>"+" "
        aux1 =', cuyos datos generales se \
                encuentran especificadas en la cláusula primera del presente contrato, quien(es) se constituye(n) en \
                GARANTE(S) PERSONAL(ES) de todas las obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> ante <b>"EL \
                ACREEDOR"</b>, y de todo lo estipulado en el presente contrato, y las inherentes y emergentes en forma \
                solidaria, mancomunada e indivisible con el(la) mismo(a) y entre sí, y en principal, liso(a) y llano(a) \
                pagador(a)(es) del préstamo, comisiones, intereses, impuestos, gastos, costas, etc., y demás cargos y \
                accesorios aplicables, renunciando de su parte a los beneficios de excusión, orden, división y otros \
                beneficios legales , aceptando para si todos los términos, comisiones y cláusulas estipuladas en el \
                presente contrato, obligándose al pago del préstamo y demás obligaciones en la misma condición y \
                calidad de obligado principal que <b>"El(la)(los) DEUDOR(A)(ES)"</b> y en forma incondicional e irrestricta.<br/> \
                Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
                obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa \
                extinguirá la garantía ni las obligaciones que <b>"El(la)(los) GARANTE(S) PERSONAL(ES) y/o DEPOSITARIO(S)"</b> asume(n) \
                en tal calidad y como codeudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
                prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>. <br/>\
                <b>"El(la)(los) GARANTE(S) PERSONAL(ES) y/o DEPOSITARIO(S)"</b> desde ya expresa(n) su acuerdo, consentimiento, sin que para \
                ello sea preciso ninguna comunicación ni aviso a <b>"El(la)(los) GARANTE(S) PERSONAL(ES) y/o DEPOSITARIO(S)"</b> ni otra \
                formalidad o requisito, considerándose para todos los fines y efectos legales que dichas prórrogas, \
                renovaciones, etc., de producirse, son de conocimiento <b>"El(la)(los) GARANTE(S) PERSONAL(ES)y/o DEPOSITARIO(S)"</b> \
                y cuenta con el acuerdo y consentimiento de éste(a).<br/>\
                <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) GARANTE(S) PERSONAL(ES)"</b> autoriza(n) que, \
                mediante una Fianza al contrato principal pueda mejorarse la garantía del préstamo solicitado sin \
                necesidad que la fianza este firmada por todos los integrantes del presente contrato.'
        texto_10_3=texto_10_3+aux1
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))

    #Convenio y garantia personal
    def _garantias_cygp(self, numeral): 
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene datos de convenio 
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        #Sacado 10.2 de convenio
        if(self.__contrato["convenio"]):
            asociacion=self.__contrato["convenio"][0]["sindicato"].upper() 
            convenio_con=self.__contrato["convenio"][0]["abreviatura"].upper()
            texto_10_2 =f' <b>10.2.</b> En forma señalada, con la garantía del(los) <b>DERECHO(S) DE LINEA</b> que posee(n) como \
                propietario(s) en <b>{asociacion}</b>, y que \
                pone a disposición de GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. de \
                acuerdo al Convenio Interinstitucional suscrito con <b>{convenio_con}</b>. Consiguientemente la(s) acción(es) de \
                línea se constituye(n) en forma incondicional e irrestricta en garantía(s), dispuestas a hacerse líquidas \
                para cubrir de forma total o parcial las obligaciones producto del presente contrato de <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna. Obligándose <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> a mantener dicha(s) línea(s) libre(s) de multas y obligaciones con su sindicato o \
                cualquier otra persona natural o jurídica.' 
            self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Convenio")

        #LLAMAMOS A LOS FIADORES
        texto_10_3 = "<b>10.3.</b> Y en especial con la Fianza personal, solidaria, mancomunada e indivisible del (la)(los) señor(a)(es)"
        fiadores = self.get_fiadores()
        i=0
        for item in fiadores:
            i+=1
            nombre_fiador = item['nombre_completo'].upper()
            numero_ci_fiador = item['ci']
            aux =f' <b>{nombre_fiador}</b> con <b>C.I. Nº</b> <b>{numero_ci_fiador}</b>'
            texto_10_3 = texto_10_3 + aux
            if (i != len(fiadores)-1):
                texto_10_3 = texto_10_3 +""
            else:
                texto_10_3 = texto_10_3 + " <b>y</b>"+" "
        aux1 =', cuyos datos generales se \
                encuentran especificadas en la cláusula primera del presente contrato, quien(es) se constituye(n) en \
                garante(s) de todas las obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> ante <b>"EL \
                ACREEDOR"</b>, y de todo lo estipulado en el presente contrato, y las inherentes y emergentes en forma \
                solidaria, mancomunada e indivisible con el(la) mismo(a) y entre sí, y en principal, liso(a) y llano(a) \
                pagador(a)(es) del préstamo, comisiones, intereses, impuestos, gastos, costas, etc., y demás cargos y \
                accesorios aplicables, renunciando de su parte a los beneficios de excusión, orden, división y otros \
                beneficios legales ,y aceptando para sí todos los términos, comisiones y cláusulas estipuladas en el \
                presente contrato, obligándose al pago del préstamo y demás obligaciones en la misma condición y \
                calidad de obligado principal que <b>"El(la)(los) DEUDOR(A)(ES)"</b> y en forma incondicional e irrestricta.<br/> \
                Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
                obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa \
                extinguirá la garantía ni las obligaciones que <b>"El(la)(los) DEUDOR(A)(ES)" y "El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> asume(n) \
                en tal calidad y como codeudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
                prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>. <b>"El(la)(los) \
                FIADOR(A)(ES) PERSONAL(ES)"</b> desde ya expresa(n) su acuerdo, consentimiento, sin que para \
                ello sea preciso ninguna comunicación ni aviso a <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> ni otra \
                formalidad o requisito, considerándose para todos los fines y efectos legales que dichas prórrogas, \
                renovaciones, etc., de producirse, son de conocimiento de <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> \
                y cuenta con el acuerdo y consentimiento de éste(a).<br/>\
                <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> autoriza(n) que, \
                mediante una Fianza al contrato principal pueda mejorarse la garantía del préstamo solicitado sin \
                necesidad que la fianza este firmada por todos los integrantes del presente contrato.'
        texto_10_3=texto_10_3+aux1
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))

    # DECIMO 2 (solo hasta el 10.2)
    def _garantias2(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene datos de convenio 
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        # LA API(http://192.168.100.5:8000/api/v1/contratos/501231701701/) DEVUEVE UN DICCIONAIO PERO EN EL ADMI SE 
        # ALMACENA COMO UN ARRAY, SE AJUSTO A LO QUE SE TIENE EN EL ADMI
        if(self.__contrato["convenio"]):
            asociacion=self.__contrato["convenio"][0]["sindicato"].upper() 
            convenio_con=self.__contrato["convenio"][0]["abreviatura"].upper()
            texto_10_2 =f' <b>10.2.</b> En forma señalada, con la garantía del(los) <b>DERECHO(S) DE LINEA</b> que posee(n) como \
                propietario(s) en <b>{asociacion}</b>, y que \
                pone a disposición de GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. de \
                acuerdo al Convenio Interinstitucional suscrito con <b>{convenio_con}</b>. Consiguientemente la(s) acción(es) de \
                línea se constituye(n) en forma incondicional e irrestricta en garantía(s), dispuestas a hacerse líquidas \
                para cubrir de forma total o parcial las obligaciones producto del presente contrato de <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna. Obligándose <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> a mantener dicha(s) línea(s) libre(s) de multas y obligaciones con su sindicato o \
                cualquier otra persona natural o jurídica.<br/>\
                Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
                obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa \
                extinguirá la garantía ni las obligaciones que asume(n), sin que afecte en ninguna forma de derecho las \
                eventuales prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/>\
                <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda \
                mejorarse la garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los \
                integrantes del presente contrato.' 
            self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Convenio")

    # DECIMO 3 (solo hasta el 10.3)
    def _garantias3(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene datos de convenio 
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        if(self.__contrato["convenio"]):
            asociacion=self.__contrato["convenio"][0]["sindicato"].upper()
            convenio_con=self.__contrato["convenio"][0]["abreviatura"].upper()
            texto_10_2 = f' <b>10.2.</b> En forma señalada, con la garantía del(los) <b>DERECHO(S) DE LINEA</b> que posee(n) como \
                propietario(s) en <b>{asociacion}</b>, y que \
                pone a disposición de GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. de \
                acuerdo al Convenio Interinstitucional suscrito con <b>{convenio_con}</b>. Consiguientemente la(s) acción(es) de \
                línea se constituye(n) en forma incondicional e irrestricta en garantía(s), dispuestas a hacerse líquidas \
                para cubrir de forma total o parcial las obligaciones producto del presente contrato de <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna. Obligándose <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> a mantener dicha(s) línea(s) libre(s) de multas y obligaciones con su sindicato o \
                cualquier otra persona natural o jurídica' 
            self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Convenio")
        matricula=self.get_matricula()
        texto_10_3 =f' <b>10.3.</b> En especial y en forma señalada, con la(s) garantía(s) de <b>DOCUMENTOS EN CUSTODIA DE \
            INMUEBLE</b>  registrado en DD.RR. bajo la <b>{matricula}</b>, bajo el siguiente detalle: ' 
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        self._parrafos.append(Spacer(0, 8))

        P0 = Paragraph('''
            <b>Nº</b>''')
        P1 = Paragraph('''
            <b>DETALLE DEL DOCUMENTO</b>''')
        P2 = Paragraph('''
            <b>FOJAS</b>''')
        t = Table([
        [P0, P1, P2]],
        colWidths=[30,230,94+1*cm], rowHeights=None
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('TOPPADDING',(0,0),(-1,-1),1),
        ])
        self._parrafos.append(t)
        estilo = getSampleStyleSheet()
        P1 = Paragraph('''El tux templario''', estilo["BodyText"])
        i=0
        t = Table(
            data=[                
                (
                    str(i)+".",                    
                    Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                    Paragraph(items["fojas"].upper(),estilos["left"])
                ) for i,items in enumerate(datos_garantias,1)
            ], 
            colWidths=[30,230,94+1*cm], rowHeights=None           
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('VALIGN', (0,0), (-1, -1), 'TOP'),    
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),         
        ])
        self._parrafos.append(t)
        linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
        self._parrafos.append(linea)
        self._parrafos.append(Spacer(0, 8))
        texto_10_3_continue ='Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
            ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/> \
            Consiguientemente los Documentos del Inmueble se constituye(n) en forma incondicional e irrestricta en \
            garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
            presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/> \
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
            la garantía ni las obligaciones que asume(n), sin que afecte en ninguna forma de derecho las eventuales \
            prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/> \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la \
            garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del \
            presente contrato.' 
        self._parrafos.append(Paragraph(texto_10_3_continue, estilos['Justify']))
    
    # DECIMO 3 (solo hasta el 10.3 para Vehiculo)
    def _garantias3V(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene datos de convenio 
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        if(self.__contrato["convenio"]):
            asociacion=self.__contrato["convenio"][0]["sindicato"].upper()
            convenio_con=self.__contrato["convenio"][0]["abreviatura"].upper()
            texto_10_2 = f' <b>10.2.</b> En forma señalada, con la garantía del(los) <b>DERECHO(S) DE LINEA</b> que posee(n) como \
                propietario(s) en <b>{asociacion}</b>, y que \
                pone a disposición de GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. de \
                acuerdo al Convenio Interinstitucional suscrito con <b>{convenio_con}</b>. Consiguientemente la(s) acción(es) de \
                línea se constituye(n) en forma incondicional e irrestricta en garantía(s), dispuestas a hacerse líquidas \
                para cubrir de forma total o parcial las obligaciones producto del presente contrato de <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna. Obligándose <b>"El(la)(los) \
                DEUDOR(A)(ES)"</b> a mantener dicha(s) línea(s) libre(s) de multas y obligaciones con su sindicato o \
                cualquier otra persona natural o jurídica'
            self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Convenio")
        placa=self.get_placa()
        texto_10_3 =f' <b>10.3.</b> En especial y en forma señalada, con la(s) garantía(s) de <b>DOCUMENTOS EN CUSTODIA DEL \
            VEHICULO</b> con <b>{placa}</b>, bajo el siguiente detalle: ' 
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        self._parrafos.append(Spacer(0, 8))
        P0 = Paragraph('''
            <b>Nº</b>''')
        P1 = Paragraph('''
            <b>DETALLE DEL DOCUMENTO</b>''')
        P2 = Paragraph('''
            <b>FOJAS</b>''')
        t = Table([
        [P0, P1, P2]],
        colWidths=[30,230,94+1*cm], rowHeights=None
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('TOPPADDING',(0,0),(-1,-1),1),
        ])
        self._parrafos.append(t)
        estilo = getSampleStyleSheet()
        P1 = Paragraph('''El tux templario''', estilo["BodyText"])
        i=0
        t = Table(
            data=[                
                (
                    str(i)+".",                    
                    Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                    Paragraph(items["fojas"].upper(),estilos["left"])
                ) for i,items in enumerate(datos_garantias,1)
            ], 
            colWidths=[30,230,94+1*cm], rowHeights=None # para modificar el ancho de las columnas
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('VALIGN', (0,0), (-1, -1), 'TOP'),  
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),           
        ])
        self._parrafos.append(t)
        linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
        self._parrafos.append(linea)
        self._parrafos.append(Spacer(0, 8))
        texto_10_3_continue ='<br/>Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
            ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/>\
            Consiguientemente los Documentos del Vehiculo se constituye(n) en forma incondicional e irrestricta en \
            garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
            presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/> \
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
            la garantía ni las obligaciones que asume(n), sin que afecte en ninguna forma de derecho las eventuales \
            prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/> \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la \
            garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del \
            presente contrato.' 
        self._parrafos.append(Paragraph(texto_10_3_continue, estilos['Justify']))
    
    # DECIMO 4 (solo hasta el 10.2)'''Solidario''' 
    def _garantias4(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        grupo=self.__contrato["descripcion_grupo"]
        texto_10_2 =f' <b>10.2.</b> En especial y en forma señalada, con la <b>GARANTIA SOLIDARIA</b>, mancomunada e indivisible, de \
            libre y espontánea voluntad y sin presión alguna pactada entre partes, sin reserva, ni limitación alguna, \
            renunciando a los beneficios de exclusión, división o cualesquier otro que puedan favorecerles a todos \
            los componentes del grupo <b>{grupo}</b>, quienes se constituyen en fiadores de todas las \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> ante <b>EL ACREEDOR</b> y estipuladas en el \
            presente contrato, y las inherentes y emergentes en forma solidaria, mancomunada e indivisible con \
            el(la) mismo(a) y entre sí, y en principal, liso y llano pagador(a)(es) del préstamo, comisiones, \
            intereses, impuestos, gastos, costas, etc., y demás cargos y accesorios aplicables, renunciando de su \
            parte a los beneficios de excusión, orden, división y otros beneficios legales, y aceptando para sí todos \
            los términos, comisiones y cláusulas estipuladas en el presente contrato, obligándose al pago del \
            préstamo y demás obligaciones en la misma condición y calidad de obligado principal que <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> en forma incondicional e irrestricta. <br/>\
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa \
            extinguirá la garantía ni las obligaciones que asume(n) en tal calidad, sin que afecte en ninguna forma \
            de derecho las eventuales prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b>. <br/>\
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda \
            mejorarse la garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los \
            integrantes del presente contrato.'
        self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
    
    def _garantias_otrosdc(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene garantias reales
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))

        texto_10_3 =f' <b>10.2.</b> En especial y en forma señalada, con la(s) garantía(s) de <b>OTROS DOCUMENTOS EN CUSTODIA</b> \
            registrado(s) bajo el siguiente detalle: '
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        self._parrafos.append(Spacer(0, 8))
        deudores=self.get_deudores()
        if(len(deudores)<=1):
            self._parrafos.append(Spacer(0, 4))
        if(len(datos_garantias)>0):
            P0 = Paragraph('''
                <b>Nº</b>''')
            P1 = Paragraph('''
                <b>DETALLE DEL DOCUMENTO</b>''')
            P2 = Paragraph('''
                <b>FOJAS</b>''')
            t = Table([
            [P0, P1, P2]],
            colWidths=[30,230,94+1*cm], rowHeights=None
            )
            t.setStyle([
                ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
                ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
                ('ALIGN',(0,-1),(-1,-1),'CENTER'),
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
                ('BOTTOMPADDING',(0,0),(-1,-1),1),
                ('TOPPADDING',(0,0),(-1,-1),1),
            ])
            self._parrafos.append(t)
            estilo = getSampleStyleSheet()
            P1 = Paragraph('''El tux templario''', estilo["BodyText"])
            i=0
            t = Table(
                data=[                
                    (
                        str(i)+".",                    
                        Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                        Paragraph(items["fojas"].upper(),estilos["left"])
                    ) for i,items in enumerate(datos_garantias,1)
                ], 
                colWidths=[30,230,94+1*cm], rowHeights=None           
            )
            t.setStyle([
                ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
                ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
                ('VALIGN', (0,0), (-1, -1), 'TOP'),  
                ('BOTTOMPADDING',(0,0),(-1,-1),0),
                ('TOPPADDING',(0,0),(-1,-1),0),           
            ])
            self._parrafos.append(t)
            linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
            self._parrafos.append(linea)
                        
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales")
        self._parrafos.append(Spacer(0, 8))
        texto_10_3_continue ='Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
            ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/>\
            Consiguientemente los Documentos del Inmueble se constituye(n) en forma incondicional e irrestricta en \
            garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
            presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/>\
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
            la garantía ni las obligaciones que asume(n) como deudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
            prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/> \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la \
            garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del \
            presente contrato.' 
        self._parrafos.append(Paragraph(texto_10_3_continue, estilos['Justify']))

    def _garantias_pampahasi(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        matricula=self.get_matricula()
        texto_10_3 =f' <b>10.2.</b> En especial y en forma señalada, con la(s) garantía(s) de <b>DOCUMENTOS EN CUSTODIA DE \
            INMUEBLE</b>  registrado en DD.RR. bajo la <b>{matricula}</b> bajo el siguiente detalle: '
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))
        #jalo al json
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        
        self._parrafos.append(Spacer(0, 8))
        deudores = self.get_deudores()
        if(len(deudores)<=1):
            self._parrafos.append(Spacer(0, 6))
        P0 = Paragraph('''
            <b>Nº</b>''')
        P1 = Paragraph('''
            <b>DETALLE DEL DOCUMENTO</b>''')
        P2 = Paragraph('''
            <b>FOJAS</b>''')
        t = Table([
        [P0, P1, P2]],
        colWidths=[30,230,94+1*cm], rowHeights=None
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('TOPPADDING',(0,0),(-1,-1),1),
        ])
        self._parrafos.append(t)
        estilo = getSampleStyleSheet()
        P1 = Paragraph('''El tux templario''', estilo["BodyText"])
        i=0
        t = Table(
            data=[                
                (
                    str(i)+".",                    
                    Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                    Paragraph(items["fojas"].upper(),estilos["left"])
                ) for i,items in enumerate(datos_garantias,1)
            ], 
            colWidths=[30,230,94+1*cm], rowHeights=None           
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('VALIGN', (0,0), (-1, -1), 'TOP'),     
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),        
        ])
        self._parrafos.append(t)
        linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
        self._parrafos.append(linea)
        self._parrafos.append(Spacer(0, 8))
        texto_10_3_continue ='Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
            ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/>\
            Consiguientemente los Documentos del Inmueble se constituye(n) en forma incondicional e irrestricta en \
            garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
            presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/> \
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
            la garantía ni las obligaciones que asume(n) como deudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
            prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/> \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la \
            garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del \
            presente contrato.' 
        self._parrafos.append(Paragraph(texto_10_3_continue, estilos['Justify']))
    
    # DECIMO 6 fafario
    def _garantias6Q(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:' 
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A. <br/>\
            Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
            obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
            la garantía ni las obligaciones que asume(n), sin que afecte en ninguna forma de derecho las eventuales \
            prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/>\
            <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la \
            garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del \
            presente contrato.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))

    # DECIMO 7
    def _garantias_pyv(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: Si no tiene garantias reales 
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
            presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        #llamamos fiadores
        fiadores = self.get_fiadores()
        if(len(fiadores)>0):
            texto_10_2 ="<b>10.2.</b> Con la Fianza personal, solidaria, mancomunada e indivisible del (la)(los) señor(a)(es) "
            j=0
            for item in fiadores:
                j+=1
                nombre_fiador = item['nombre_completo'].upper()
                numero_ci_fiador = item['ci'] 
                auxfiador=f'<b>{nombre_fiador}</b> con C.I. Nº <b>{numero_ci_fiador}</b>'
                texto_10_2 = texto_10_2 + auxfiador
                if (j != len(fiadores)-1):
                    texto_10_2 = texto_10_2 + ","+" "
                else:
                    texto_10_2 = texto_10_2 + " y"+" "
            aux =' cuyos datos generales se \
            encuentran especificadas en la cláusula primera del presente contrato, quien(es) se constituye(n) en \
            garante(s) de todas las obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> ante <b>"EL \
            ACREEDOR"</b>, y de todo lo estipulado en el presente contrato, y las inherentes y emergentes en forma \
            solidaria, mancomunada e indivisible con el(la) mismo(a) y entre sí, y en principal, liso(a) y llano(a) \
            pagador(a)(es) del préstamo, comisiones, intereses, impuestos, gastos, costas, etc., y demás cargos y \
            accesorios aplicables, renunciando de su parte a los beneficios de excusión, orden, división y otros \
            beneficios legales ,y aceptando para sí todos los términos, comisiones y cláusulas estipuladas en el \
            presente contrato, obligándose al pago del préstamo y demás obligaciones en la misma condición y \
            calidad de obligado principal que <b>"El(la)(los) DEUDOR(A)(ES)"</b> y en forma incondicional e irrestricta.'
            texto_10_2=texto_10_2+aux
            self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales")

        placa=self.get_placa()
        texto_10_3 =f' <b>10.3.</b> Y en especial y en forma señalada, con la(s) garantía(s) de <b>DOCUMENTOS EN CUSTODIA DEL \
        VEHICULO</b> con <b>"{placa}</b> y bajo el siguiente detalle: ' 
        self._parrafos.append(Paragraph(texto_10_3, estilos['Justify']))
        #jalo al json
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        self._parrafos.append(Spacer(0, 8))

        P0 = Paragraph('''
            <b>Nº</b>''')
        P1 = Paragraph('''
            <b>DETALLE DEL DOCUMENTO</b>''')
        P2 = Paragraph('''
            <b>FOJAS</b>''')
        t = Table([
        [P0, P1, P2]],
        colWidths=[30,230,94+1*cm], rowHeights=None
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('TOPPADDING',(0,0),(-1,-1),1),
        ])
        self._parrafos.append(t)
        estilo = getSampleStyleSheet()
        P1 = Paragraph('''El tux templario''', estilo["BodyText"])
        i=0
        t = Table(
            data=[                
                (
                    str(i)+".",                    
                    Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                    Paragraph(items["fojas"].upper(),estilos["left"])
                ) for i,items in enumerate(datos_garantias,1)
            ], 
            colWidths=[30,230,94+1*cm], rowHeights=None           
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('VALIGN', (0,0), (-1, -1), 'TOP'), 
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),            
        ])
        self._parrafos.append(t)
        linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
        self._parrafos.append(linea)
        self._parrafos.append(Spacer(0, 8))
        texto_10_3_continue ='Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
        ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/>\
        Consiguientemente los Documentos del Inmueble se constituye(n) en forma incondicional e irrestricta en \
        garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
        presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/>\
        Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
        obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
        la garantía ni las obligaciones que <b>"El(la)(los) DEUDOR(A)(ES)"</b> y <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> asumen, en tal calidad y como codeudor(a)(es), sin que afecte en ninguna forma de derecho las eventuales \
        prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>. \
        <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> desde ya expresa(n) su acuerdo, consentimiento, sin que para ello sea preciso ninguna comunicación ni aviso a <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> ni otra formalidad o requisito, considerándose para todos los fines y efectos legales que dichas prórrogas, renovaciones, etc., de producirse, son de conocimiento de <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> y cuenta con el acuerdo y consentimiento de éste(a).<br/> \
        <b>"El(la)(los) DEUDOR(A)(ES)"</b> y/o <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda mejorarse la garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los integrantes del presente contrato.' 
        self._parrafos.append(Paragraph(texto_10_3_continue, estilos['Justify']))

    #GARANTIA DOCUMENTOS EN CUSTODIA VEHICULO
    def _garantias8dcv(self, numeral):
        """
        Esta funcion añade: GARANTIAS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """   
        texto = f'<b><u>{numeral}</u>.- (GARANTIAS).- "El(la)(los) DEUDOR(A)(ES)"</b> garantiza(n) el fiel y estricto cumplimiento del \
        presente contrato y de todas las obligaciones señaladas, inherentes y emergentes al mismo de la \
        siguiente manera:'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        texto_10_1 = '<b>10.1.</b> Con la generalidad de sus bienes, mercaderías, muebles e inmuebles, presentes descritas en el \
            formulario "Declaración Patrimonial" que forma parte íntegra del presente contrato sin necesidad de ser \
            transcrito, bienes, mercaderías, muebles e inmuebles, futuros sin exclusión ni limitación alguna. <b>"El(la)(los) \
            DEUDOR(A)(ES)"</b> se obliga(n) a no vender, ceder, transferir, etc., bajo ningún título los bienes \
            descritos en el formulario de Declaración Patrimonial, mientras perdure la obligación con GESTION Y \
            SOPORTE DE PROYECTOS JESUS DEL GRAN PODER S.A.'
        self._parrafos.append(Paragraph(texto_10_1, estilos['Justify']))
        placa=self.get_placa()
        texto_10_2 =f' <b>10.2.</b> En especial y en forma señalada, con la(s) garantía(s) de <b>DOCUMENTOS EN CUSTODIA DEL \
            VEHÍCULO</b> con <b>{placa}</b>, bajo el siguiente detalle: ' 
        self._parrafos.append(Paragraph(texto_10_2, estilos['Justify']))
        datos_garantias = self.__contrato["garantias_reales"]=self.filtrar_datos()
        self._parrafos.append(Spacer(0, 8))
        deudores = self.get_deudores()
        if(len(deudores)<=1):
            self._parrafos.append(Spacer(0, 6))

        P0 = Paragraph('''
            <b>Nº</b>''')
        P1 = Paragraph('''
            <b>DETALLE DEL DOCUMENTO</b>''')
        P2 = Paragraph('''
            <b>FOJAS</b>''')
        t = Table([
        [P0, P1, P2]],
        colWidths=[30,230,94+1*cm], rowHeights=None
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
            ('BOTTOMPADDING',(0,0),(-1,-1),1),
            ('TOPPADDING',(0,0),(-1,-1),1),
        ])
        self._parrafos.append(t)
        t = Table(
            data=[                
                (
                    str(i)+".",                    
                    Paragraph(items["concepto"].upper()+" "+items["detalle_garantia"].upper(),estilos["left"]),
                    Paragraph(items["fojas"].upper(),estilos["left"])
                ) for i,items in enumerate(datos_garantias,1)
            ], 
            colWidths=[30,230,94+1*cm], rowHeights=None          
        )
        t.setStyle([
            ('LINEABOVE', (0,0), (-1, 0), 1, colors.black),
            ('INNERGRID', (-10,-5), (-20,-13), 0.65, colors.black),
            ('VALIGN', (0,0), (-1, -1), 'TOP'),   
            ('BOTTOMPADDING',(0,0),(-1,-1),0),
            ('TOPPADDING',(0,0),(-1,-1),0),         
        ])
        self._parrafos.append(t)
        linea=Table(data=[''],colWidths=13.5*cm,rowHeights=0.02*cm,style=[('LINEABOVE',(0, 0), (-1, 0),1,colors.black)])
        self._parrafos.append(linea)
        self._parrafos.append(Spacer(0, 8))
        texto_10_2_continue ='Documentos originales de propiedad de <b>"El(la)(los) DEUDOR(A)(ES)"</b> y depositados en las oficinas de <b>"EL \
        ACREEDOR"</b> bajo libre y espontánea voluntad y sin presión alguna por parte del(la)(los) propietario(a)(s).<br/>\
        Consiguientemente los Documentos del Vehículo se constituye(n) en forma incondicional e irrestricta en \
        garantía(s), dispuesta(s) a hacerse liquida para cubrir de forma total o parcial las obligaciones producto del \
        presente contrato de <b>"El(la)(los) DEUDOR(A)(ES)"</b> con <b>"EL ACREEDOR"</b>, sin reserva, ni limitación alguna.<br/>\
        Queda establecido que mientras no se haga efectivo el pago total y definitivo de la deuda y demás \
        obligaciones asumidas por <b>"El(la)(los) DEUDOR(A)(ES)"</b> en el presente contrato, ninguna causa extinguirá \
        la garantía ni las obligaciones que asume(n) como deudor(a)(es), sin que afecte en ninguna \
        forma de derecho las eventuales prorrogas o renovaciones que <b>"EL ACREEDOR"</b> concediera a <b>"El(la)(los) DEUDOR(A)(ES)"</b>.<br/>  \
        <b>"El(la)(los) DEUDOR(A)(ES)"</b> autoriza(n) que, mediante una Fianza al contrato principal pueda\
        mejorarse la garantía del préstamo solicitado sin necesidad que la fianza este firmada por todos los\
        integrantes del presente contrato.'
        self._parrafos.append(Paragraph(texto_10_2_continue, estilos['Justify']))

    def get_prendaria(self):
        """
        Esta funcion busca el concepto de Descripcion y obtiene el valor de detalle_garantia.
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: Los objetos dejados en garantia
        Raises:
            ContratoError: Si no tiene garantia por concepto de Descripcion
        """   
        garantias=self.__contrato["garantias_reales"]
        sw=False
        for item in garantias:
            if(item['concepto']=="Descripcion"):
                prendaria=item['detalle_garantia']  
                sw=True
        if(sw==False):
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de la garantia por concepto de: Descripción")
        return prendaria

    def get_direccion_g(self):
        """
        Esta funcion busca el concepto de Ubicacion y obtiene el valor de detalle_garantia.
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: La direccion de los objetos dejados en garantia
        Raises:
            ContratoError: Si no tiene garantia por concepto de Descripcion
        """
        garantias=self.__contrato["garantias_reales"]
        sw=False
        for item in garantias:
            if(item['concepto']=="Ubicacion"):
                ubicacion=item['detalle_garantia']
                sw=True 
        if(sw==False):
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de la garantia por concepto de: Ubicación")            
        return ubicacion.upper()
        
    #METODOS PARA detalle_garantia
    def isNumeric(self,valor):
        """
        Esta funcion valida si es un numero entero o no.
        Args:
            - valor (String): Es un String el cual es enviado para validar si es numero o no
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            bool: retorna True si es un numero y False no no es un numero
        """
        try:
            int(valor)
            return True
        except ValueError:
            return False

    def detalleGarantia(self, descripcion):
        """
        Esta funcion convierte los numeros que haya en descripcion en letras.
        Args:
            - descripcion (String): las prendas dejadas en garantia 
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: Retorna la descripcion de las garantias y si hay numeros lo transforma en literal
        """
        array= descripcion.split(', ')
        StrA=""
        for i,x in enumerate(array,0):
            array_num=x.split(' ')
            if(self.isNumeric(array_num[0])):
                num=int(array_num[0])           
                if(num==1):
                    literal="un(a)"
                else:
                    literal=Utils.literalNumeral(num)
                    literal=literal.lower()
                array_num[0]=literal
                if(i!=len(array)-1):
                    StrA = StrA+" ".join(array_num)+", "
                else:
                    StrA = StrA+" ".join(array_num)
        if(StrA==""):
            return descripcion
        else:
            return StrA    
    
    def _supervision(self, numeral):
        """
        Esta funcion añade: SUPERVISION Y VISITAS DE INSPECCION E INFORMACION, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """ 
        texto = f'<b><u>{numeral}</u>.- (SUPERVISION Y VISITAS DE INSPECCION E INFORMACION).-  "EL \
            ACREEDOR"</b> tiene el más amplio derecho para supervisar, inspeccionar y constatar periódicamente,\
            por medio de sus propios inspectores o por delegados contratados, la veracidad de la información \
            proporcionada por <b>"El(la)(los) DEUDOR(A)(ES)"</b>. Las partes se obligan a facilitar todas y cada una de \
            las labores de supervisión, inspección o control que <b>"EL ACREEDOR"</b> estime por conveniente.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))

    def _cesion_obligacion(self, numeral):
        """
        Esta funcion añade: CESION DE LA OBLIGACION, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """ 
        texto = f'<b><u>{numeral}</u>.- (CESION DE LA OBLIGACION).-  "El(la)(los) DEUDOR(A)(ES)"</b>, acepta(n) \
            incondicionalmente que <b>"EL ACREEDOR"</b> pueda transferir, ceder pignorar o delegar a terceros la \
            presente obligación, cesión o transferencia que se operará sin necesidad del permiso expreso por \
            <b>"El(la)(los) DEUDOR(A)(ES)"</b>, limitando su accionar a comunicar dicha cesión al domicilio señalado en \
            la cláusula primera.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    def _autorizacion(self, numeral):
        """
        Esta funcion añade: AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """ 
        texto = f'<b><u>{numeral}</u>.- (AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS).- \
            "El(la)(los) DEUDOR(A)(ES)" y "El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>, autoriza(n) en forma \
            expresa a GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. a solicitar \
            información sobre sus antecedentes crediticios y otras cuentas por pagar de carácter económico, \
            financiero y comercial registrados en el BI y la CIC de la Autoridad de Supervisión del Sistema \
            Financiero (ASFI), mientras dure su relación contractual con el citado usuario.<br/>\
            Asimismo, autoriza(n):'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = '<bullet></bullet> Incorporar los datos crediticios y de otras cuentas por pagar de carácter económico, financiero y \
            comercial derivados de la relación con GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL \
            GRAN PODER S.A., en la(s) base(s) de datos de propiedad de los Burós de Información que \
            cuenten con Licencia de Funcionamiento de ASFI y en la CIC.' 
        b = '<bullet></bullet> Al registro de sus datos crediticios en las bases de datos de INFOCENTER S.A, con licencia de \
            funcionamiento del Organismo de Supervisión, ASFI.' 
        incisos = ListFlowable(
        [
            Paragraph(a,estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                        
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20
        )
        self._parrafos.append(incisos)
    
    #12
    def _autorizacion4(self, numeral):
        """
        Esta funcion añade: AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS).- \
            "El(la)(los) DEUDOR(A)(ES)" y "El(la)(los) GARANTE(S) PERSONAL(ES)"</b>, autoriza(n) en forma \
            expresa a GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A. a solicitar \
            información sobre sus antecedentes crediticios y otras cuentas por pagar de carácter económico, \
            financiero y comercial registrados en el BI y la CIC de la Autoridad de Supervisión del Sistema \
            Financiero (ASFI), mientras dure su relación contractual con el citado usuario.<br/>\
            Asimismo, autoriza(n):'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = '<bullet></bullet> Incorporar los datos crediticios y de otras cuentas por pagar de carácter económico, financiero y \
            comercial derivados de la relación con GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL \
            GRAN PODER S.A., en la(s) base(s) de datos de propiedad de los Burós de Información que \
            cuenten con Licencia de Funcionamiento de ASFI y en la CIC.' 
        b = '<bullet></bullet> Al registro de sus datos crediticios en las bases de datos de INFOCENTER S.A, con licencia de \
            funcionamiento del Organismo de Supervisión, ASFI.' 
        incisos = ListFlowable(
        [
            Paragraph(a,estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                        
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20
        )
        self._parrafos.append(incisos)

    #DÉCIMA TERCERA 2 
    def _autorizacion2(self, numeral):
        """
        Esta funcion añade: AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS).- "El(la)(los) \
            DEUDOR(A)(ES)"</b> autoriza(n) en forma expresa a GESTIÓN Y SOPORTE DE PROYECTOS JESÚS \
            DEL GRAN PODER S.A. a solicitar información sobre sus antecedentes crediticios y otras cuentas por pagar \
            de carácter económico, financiero y comercial registrados en el BI y la CIC de la Autoridad de Supervisión \
            del Sistema Financiero (ASFI), mientras dure su relación contractual con el citado usuario.<br/>\
            Asimismo, autoriza(n):'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = 'Incorporar los datos crediticios y de otras cuentas por pagar de carácter económico, financiero y \
            comercial derivados de la relación con GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL \
            GRAN PODER S.A., en la(s) base(s) de datos de propiedad de los Burós de Información que \
            cuenten con Licencia de Funcionamiento de ASFI y en la CIC.' 
        b = 'Al registro de sus datos crediticios en las bases de datos de INFOCENTER S.A, con licencia de \
            funcionamiento del Organismo de Supervisión, ASFI.' 
        incisos = ListFlowable(
        [
            Paragraph(a, estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                           
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20        
        )
        self._parrafos.append(incisos)
    
    #DÉCIMA TERCERA 3'''Personal y Documentos en Custodia de Vehículo'''
    def _autorizacion3(self, numeral):
        """
        Esta funcion añade: AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (AUTORIZACION DE INVESTIGACION DE ANTECEDENTES CREDITICIOS).- "El(la) \
            (los) DEUDOR(A)(ES)"</b> y <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b>, autoriza(n) en forma expresa a GESTIÓN Y SOPORTE DE PROYECTOS JESÚS \
            DEL GRAN PODER S.A. a solicitar información sobre sus antecedentes crediticios y otras cuentas por pagar \
            de carácter económico, financiero y comercial registrados en el BI y la CIC de la Autoridad de Supervisión \
            del Sistema Financiero (ASFI), mientras dure su relación contractual con el citado usuario.<br/>\
            Asimismo, autoriza(n):'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        a = 'Incorporar los datos crediticios y de otras cuentas por pagar de carácter económico, financiero y \
            comercial derivados de la relación con GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL \
            GRAN PODER S.A., en la(s) base(s) de datos de propiedad de los Burós de Información que \
            cuenten con Licencia de Funcionamiento de ASFI y en la CIC.' 
        b = 'Al registro de sus datos crediticios en las bases de datos de INFOCENTER S.A, con licencia de \
            funcionamiento del Organismo de Supervisión, ASFI.' 
        incisos = ListFlowable(
        [
            Paragraph(a, estilos['Inciso']),
            Paragraph(b, estilos['Inciso']),                           
        ],            
        bulletType='a',
        bulletFormat='%s)',
        leftIndent=40,
        bulletColor='black',
        bulletFontName='Helvetica-Bold',
        bulletFontSize=tamanio_letra,
        bulletOffsetY=0,
        bulletDedent=20        
        )
        self._parrafos.append(incisos)
    
    def _titulo_ejecutivo(self, numeral):
        """
        Esta funcion añade: TITULO EJECUTIVO, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (TITULO EJECUTIVO).-</b>  El presente documento de préstamo de dinero servirá de \
            título ejecutivo y dará lugar al cobro judicial respectivo, conforme a lo establecido por el Código \
            Procesal Civil Ley N°439.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    # DÉCIMA QUINTA
    def _gastos(self, numeral):      
        """
        Esta funcion añade: GASTOS, TRIBUTOS Y SERVICIOS CONEXOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        monto1=float(self.__contrato["monto_cargos"])
        monto = Utils.literalEnteroMontoPrestamo(monto1)#monto='Bs. 140,00.- (CIENTO CUARENTA  00/100 BOLIVIANOS)'
        texto = f'<b><u>{numeral}</u>.- (GASTOS, TRIBUTOS Y SERVICIOS CONEXOS).-</b>  Todos los gastos, impuestos, \
            timbres, derechos y otros similares que corresponda aplicar a este contrato y sus emergencias, serán \
            pagados por <b>"EL ACREEDOR"</b>, sin exclusión alguna.<br/>\
            Sin perjuicio de lo expresado en el párrafo anterior, será de responsabilidad del(la)(los) DEUDOR(A)(ES)\
            los servicios de la evaluación de la capacidad de pago, endeudamiento, consulta de historial \
            crediticio, reconocimiento de firmas y rúbricas, recordatorio de pagos, citaciones, cobranzas "in situ" y \
            otros, mismo que asciende a <b>{monto}</b> que el(la)(los) \
            prestatario(a)(s) solicita(n) sea(n) diferido(s) en las cuotas del plan de pagos.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    # DÉCIMA QUINTA solidario
    def _gastos_solidario(self, numeral): 
        """
        Esta funcion añade: GASTOS, TRIBUTOS Y SERVICIOS CONEXOS, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        monto1=float(self.__contrato["monto_cargos"])
        monto = Utils.literalEnteroMontoPrestamo(monto1)#monto='Bs. 140,00.- (CIENTO CUARENTA  00/100 BOLIVIANOS)'
        texto = f'<b><u>{numeral}</u>.- (GASTOS, TRIBUTOS Y SERVICIOS CONEXOS).-</b>  Todos los gastos, impuestos, \
            timbres, derechos y otros similares que corresponda aplicar a este contrato y sus emergencias, serán \
            pagados por <b>"EL ACREEDOR"</b>, sin exclusión alguna.<br/>\
            Sin perjuicio de lo expresado en el párrafo anterior, será de responsabilidad de los DEUDORES\
            los servicios de la evaluación de la capacidad de pago, endeudamiento, consulta de historial \
            crediticio, reconocimiento de firmas y rúbricas, recordatorio de pagos, citaciones, cobranzas "in situ" y \
            otros, mismo que asciende a <b>{monto}</b> que los \
            prestatarios solicitan sean diferidos en las cuotas del plan de pagos.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    # DÉCIMA SEXTA   
    def _derechos_deudor(self, numeral):
        """
        Esta funcion añade: DERECHOS DE "El(la)(los) DEUDOR(A)(ES)", con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (DERECHOS DE "El(la)(los) DEUDOR(A)(ES)").-  "El(la)(los) DEUDOR(A)(ES)"</b> \
            tiene(n) derecho a recibir periódicamente o a solicitud, información relacionada al desglose de los \
            cobros, actualización del cronograma de pagos y forma de cálculo de los cargos financieros, etc.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
        
    # DÉCIMA SEPTIMA
    def _domicilio_especial(self, numeral):
        """
        Esta funcion añade: DOMICILIO ESPECIAL, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        texto = f'<b><u>{numeral}</u>.- (DOMICILIO ESPECIAL).-</b>  A los efectos de la ejecución y cumplimiento del \
            presente contrato, incluidas sus emergencias judiciales, como ser citaciones, notificaciones y otras \
            similares, se señala como domicilios especiales los detallados en la cláusula primera del presente \
            contrato, de conformidad a lo dispuesto por el Art. 29-II) del Código Civil, los que serán los únicos \
            válidos para ejercer y realizar cualquier acto o hecho jurídico derivado del presente contrato, no \
            pudiendo cambiar los mismos, sin que previamente se comunique tal hecho a <b>"EL ACREEDOR"</b> por \
            escrito y mediante carta notariada.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    # DÉCIMA OCTAVA
    def _aceptacion(self, numeral):
        """
        Esta funcion añade: DE LA ACEPTACION, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: si no tiene fiadores
        """
        testimonio_poder= self.__contrato["testimonio_poder"]  
        nombre_j=self.nombreCompleto_repre()
        cargo = testimonio_poder["representante_legal"]["rol"]        
        fecha_desembolso = Utils.get_fecha(self, self.__contrato["fecha_desembolso"])
        texto = f'<b><u>{numeral}</u>.- (DE LA ACEPTACION).-</b>  Nosotros: <b>"EL ACREEDOR"</b>, representado por <b>{nombre_j}</b> en su condición de {cargo}, por una parte; por otra, '
        deudores = self.get_deudores()
        i=0
        for item in deudores:
            i+=1
            nombreDeudor = item['nombre_completo'].upper()
            aux ='<b>%s</b>' % (nombreDeudor)
            texto = texto + aux
            if (i != len(deudores)-1):
                texto = texto + ","+" "
            else:
                texto = texto + " <b>y</b>"+" "
        aux1='como <b>"El(la)(los) DEUDOR(A)(ES)"</b>; y finalmente'
        texto = texto+aux1
        fiadores = self.get_fiadores() # Objengo los fiadores
        if(len(fiadores)>0):
            i=0
            for item in fiadores:
                i+=1
                nombreFiador = item['nombre_completo'].upper()
                aux =f' <b>{nombreFiador}</b>'
                texto = texto + aux
                if (i != len(fiadores)-1):
                    texto = texto + ","+" "
                else:
                    texto = texto + " <b>y</b>"+" "
            aux2=f'como <b>"El(la)(los) FIADOR(A)(ES) PERSONAL(ES)"</b> solidario(s), mancomunado(s) e \
                indivisible(s); sin que haya mediado vicio alguno del consentimiento, aceptan y expresan su entera y \
                absoluta conformidad con el tenor y contenido del presente contrato y se obligan a su más fiel y estricto \
                cumplimiento, por lo que firman en señal de aceptación.<br/>\
                LA PAZ, {fecha_desembolso}'
            texto=texto+aux2
            self._parrafos.append(Paragraph(texto, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Fiadores")
    
    #12
    def _aceptacion3(self, numeral):
        """
        Esta funcion añade: DE LA ACEPTACION, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        Raises:
            ContratoError: si no tiene fiadores
        """
        testimonio_poder= self.__contrato["testimonio_poder"]  
        nombre_j=self.nombreCompleto_repre()
        cargo = testimonio_poder["representante_legal"]["rol"]        
        fecha_desembolso = Utils.get_fecha(self, self.__contrato["fecha_desembolso"])
        texto = f'<b><u>{numeral}</u>.- (DE LA ACEPTACION).-</b>  Nosotros: <b>"EL ACREEDOR"</b>, representado por <b>{nombre_j}</b> en su condición de {cargo}, por una parte; por otra, '
        deudores = self.get_deudores()
        i=0
        for item in deudores:
            i+=1
            nombreDeudor = item['nombre_completo'].upper()
            aux ='<b>%s</b>' % (nombreDeudor)
            texto = texto + aux
            if (i != len(deudores)-1):
                texto = texto + ","+" "
            else:
                texto = texto + " <b>y</b>"+" "
        aux1='como <b>"El(la)(los) DEUDOR(A)(ES)"</b>; y finalmente'
        texto = texto+aux1
        fiadores = self.get_fiadores()# Objengo los fiadores
        if(len(fiadores)>0):
            i=0
            for item in fiadores:
                i+=1
                nombreFiador = item['nombre_completo'].upper()
                aux =f' <b>{nombreFiador}</b>'
                texto = texto + aux
                if (i != len(fiadores)-1):
                    texto = texto + ","+" "
                else:
                    texto = texto + " <b>y</b>"+" "
            aux2=f'como <b>"El(la)(los) GARANTE(S) PERSONAL(ES) y/o DEPOSITARIO(S)"</b> solidario(s), mancomunado(s) e \
                indivisible(s); sin que haya mediado vicio alguno del consentimiento, aceptan y expresan su entera y \
                absoluta conformidad con el tenor y contenido del presente contrato y se obligan a su más fiel y estricto \
                cumplimiento, por lo que firman en señal de aceptación.<br/>\
                LA PAZ, {fecha_desembolso}'
            texto=texto+aux2
            self._parrafos.append(Paragraph(texto, estilos['Justify']))
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de Fiadores")

    #DÉCIMA OCTAVA 2
    '''Para todos, menos Personal y Documentos en Custodia de Vehículo'''
    def _aceptacion2(self, numeral):
        """
        Esta funcion añade: DE LA ACEPTACION, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """
        testimonio_poder= self.__contrato["testimonio_poder"]  
        nombre_j=self.nombreCompleto_repre()
        cargo = testimonio_poder["representante_legal"]["rol"]        
        fecha_desembolso = Utils.get_fecha(self, self.__contrato["fecha_desembolso"])
        #llamamos a los deudores
        texto = f'<b><u>{numeral}</u>.- (DE LA ACEPTACION).-</b>  Nosotros: <b>"EL ACREEDOR"</b>, representado por <b>{nombre_j}</b> en su condición de {cargo}, por una parte; por otra, '
        deudores = self.get_deudores()
        i=0
        for item in deudores:
            i+=1
            nombreDeudor = item['nombre_completo'].upper()
            aux ='<b>%s</b>' % (nombreDeudor)
            texto = texto + aux
            if (i != len(deudores)-1):
                texto = texto + ","+" "
            else:
                texto = texto + " <b>y</b>"+" "
        aux1= f'como <b>"El(la)(los) DEUDOR(A)(ES)"</b>; sin que haya mediado vicio alguno del consentimiento, aceptan y expresan su entera y \
            absoluta conformidad con el tenor y contenido del presente contrato y se obligan a su más fiel y estricto \
            cumplimiento, por lo que firman en señal de aceptación.<br/>\
            LA PAZ, {fecha_desembolso}'
        texto = texto+aux1
        self._parrafos.append(Paragraph(texto, estilos['Justify']))

    #PRIMERA 2
    def nombreCompleto_repre(self):
        """
        Esta funcion concatena el nombre completo del representante legal
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: El nombre completo del representante legal en mayuscula
        """
        nombre = (self.__contrato["testimonio_poder"]["representante_legal"]["first_name"]+" "+self.__contrato["testimonio_poder"]["representante_legal"]["last_name"]).upper()
        return nombre
    
    def get_deudores(self):   
        """
        Esta funcion obtiene los deudores en un array es decir aquellos que sean de tipo_obligado: 1A, 14, 5A, 1B
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            array: Con todos los deudores
        Raises:
            ContratoError: si no tiene deudores
        """
        deudores=self.__contrato["deudores"]     
        if(len(deudores)>0):
            deudores_ = [item for item in deudores if (item["tipo_obligado"]=="1A" or item["tipo_obligado"]=="4A" or item["tipo_obligado"]=="5A" or item["tipo_obligado"]=="1B")]
            return deudores_
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los dados del(los) Deudor(es)")
    
    def get_estado_civil(self,_estado_civil, genero):
        """
        Esta funcion crea un string el cual contiene el estado civil de la persona segun sus sexo
        Args:
            - self  : Un json (diccionario) y un usuario (string)
            - _estado_civil (char): S = Soltero, C = Casado, V = Viuda, D = Divorciado, N = Soltero
            - genero (char): F = Femenino, M = Masculino
        Returns:
            string: El estado civil segun su sexo
        """
        estados_civiles = {"S": "solter","C": "casad","V": "viud","D": "divorciad", "N":"solter"} # diccionario para comprobar
        if(genero =="F"): 
            return estados_civiles.get(_estado_civil) +"a"
        else:
            return estados_civiles.get(_estado_civil) +"o"

    def get_articulo_direccion(self,direccion_dato):
        """
        Esta funcion añade el articulo de la direccion
        Args:
            - self  : Un json (diccionario) y un usuario (string)
            - direccion_dato (string): La direccion de la persona
        Returns:
            string: El articulo y la direccion
        """  
        direccion = direccion_dato.split(' ')
        direccion_uno= direccion[0].lower()
        articulo=""
        if(direccion_uno =="avenida" or direccion_uno =="calle" or direccion_uno =="av." or direccion_uno =="av"): 
            articulo = "la "
        if(direccion_uno =="pasaje" or direccion_uno =="callejon" or direccion_uno =="psje." or direccion_uno =="pje."): 
            articulo = "el "
        return articulo + direccion_dato
        
    
    #funcion para retornar el numero de matricula
    def get_matricula(self):
        """
        Esta funcion obtiene el concepto y la matricula
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: El concepto + matricula o partida
        Raises:
            ContratoError: si no tiene grarantias reales por concepto: Matricula o Partida | ContratoError: si no tiene grarantias reales 
        """
        garantias=self.__contrato["garantias_reales"]
        if(len(garantias)>0):
            sw=False
            for item in garantias:
                if(item['concepto']=="Matricula" or item['concepto']=="Partida"):
                    concepto=item['concepto']
                    matricula=item['detalle_garantia']  
                    sw=True
            if(sw==False):
                raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales por Concepto: Matricula o Partida (depende del tipo de garantia)")
            return concepto+" "+matricula
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales")
        
    def get_placa(self): 
        """
        Esta funcion obtiene la Placa
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            string: El concepto +  numero de Placa
        Raises:
            ContratoError: si no tiene grarantias reales por concepto: Placa | ContratoError: si no tiene grarantias reales 
        """
        datos_garantias = self.__contrato["garantias_reales"]
        if(len(datos_garantias)>0):
            sw=False
            for item in datos_garantias:
                if(item['concepto']=="Placa"):
                    concepto=item['concepto']
                    placa=item['detalle_garantia']   
                    sw=True
            if(sw==False):
                raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales por Concepto: Placa")
            return concepto+" Nº "+placa
        else:
            raise ContratoError("Campo requerido", "El contrato requiere los Datos de garantias reales")

    def filtrar_datos(self):  
        """
        Esta funcion elimina el Concepto: Placa o Matricula o Partida
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            array: De las garantias reales que no sean por Concepto: Placa o Matricula o Partida
        """
        garantias_reales = self.__contrato["garantias_reales"] # Eliminar la garantía con el concepto "Placa" del conjunto de garantías reales
        conceptos_eliminar = ["Placa", "Matricula", "Partida"] # Definir los conceptos a eliminar
        # Filtrar las garantías reales para eliminar las que tienen los conceptos especificados
        garantias_reales = [garantia for garantia in garantias_reales if garantia["concepto"] not in conceptos_eliminar] # Actualizar los datos JSON sin la garantía eliminada
        return garantias_reales
        
    #DÉCIMA PRIMERA 1(faltante)
    def _prohibiciones(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título la(s) acción(es) dada(s) en \
            garantía(s), total ni parcialmente, así como a no constituir sobre la(s) misma(s) ningún otro derecho \
            especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    def _prohibiciones_pyp(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título el(los) bien(es) dado(s) en garantía, total ni parcialmente,\
            así como a no constituir sobre el(los) mismo(s) ningún otro derecho especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))

    #DÉCIMA PRIMERA 2(faltante)
    def _prohibiciones2(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título la(s) acción(es) ni el(los) bien(es) mueble(s) dados en garantías mediante convenio interinstitucional y con los documentos en custodia, total ni parcialmente, \
            así como a no constituir sobre las mismas ningún otro derecho \
            especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    #DÉCIMA PRIMERA 2(faltante)
    def _prohibiciones_pampahasi(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A) (ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título el(los) bien(es) inmueble(s) \
            dado(s) en garantía con los documentos en custodia, total ni parcialmente, \
            así como a no constituir sobre el(los) mismo(s) ningún otro derecho \
            especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    #DÉCIMA PRIMERA 3(faltante)
    def _prohibiciones3(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>,\
            se obliga(n) a no transferir, ceder y/o gravar a ningún título el(los) bien(es) mueble(s) dado(s) en garantía con los documentos en custodia, total ni parcialmente, \
            así como a no constituir sobre el(los) mismo(s) ningún otro derecho especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    def _prohibiciones_con_inmueble(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título la(s) acción(es) ni el(los) bien(es) \
            inmueble(s) dado(s) en garantías mediante convenio interinstitucional y con los documentos en custodia, total ni parcialmente, \
            así como a no constituir sobre las mismas ningún otro derecho especial a favor de \
            terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))

    #DÉCIMA PRIMERA 3(faltante)
    def _prohibiciones_otroscyv(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A) (ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título el(los) bien(es) inmueble(s) dado(s) en garantía con los documentos en custodia, total ni parcialmente, \
            así como a no constituir sobre el(los) mismo(s) ningún otro derecho especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))

    def _prohibiciones4(self, numeral):
        """
        Esta funcion añade: PROHIBICIONES AL DERECHO DE PROPIEDAD, con el numero de clausula correspondiente
        Args:
            - numeral (String): Es un String el cual especifica el numero de la clausula 
            - self  : Un json (diccionario) y un usuario (string)
        """  
        texto = f'<b><u>{numeral}</u>.- (PROHIBICIONES AL DERECHO DE PROPIEDAD).-  "El(la)(los) DEUDOR(A)(ES)"</b>, \
            se obliga(n) a no transferir, ceder y/o gravar a ningún título el(los) bien(es) mueble(s) dado(s) en garantía, total ni parcialmente,\
            así como a no constituir sobre el(los) mismo(s) ningún otro derecho especial a favor de terceras personales naturales o jurídicas, sin la expresa autorización escrita de <b>“EL \
            ACREEDOR"</b>.'
        self._parrafos.append(Paragraph(texto, estilos['Justify']))
    
    
    def get_fiadores(self): 
        """
        Esta funcion obtiene a los fiadores que existen
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            array: Los fiadores que habia en el json
        """   
        deudores = self.__contrato["deudores"]     
        fiadores = [item for item in deudores if item['tipo_obligado']=='2A']
        return fiadores
    
    # FIRMAS
    def _firmas(self):
        """
        Esta funcion dibuja las firmas y asi tambien el salto de pagina o añadir espacio en caso que lo requiera segun el tipo de garantia
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        """ 
        tipo_garantia=self.__contrato["tipo_garantia"]["descripcion"]
        print(tipo_garantia) 
        fiadores= self.get_fiadores()
        deudores= self.get_deudores()    
        self._parrafos.append(Spacer(0,15))
        # Modi para Prendaria y Personal  &  Personal y  Doc. custodia Vehiculo
        if((tipo_garantia=="Prendaria y Personal" and (len(deudores)>=3)) or (tipo_garantia=="Personal y  Doc. custodia Vehiculo" and (len(deudores)>=3))):
            a=self._parrafos.append
            a(PageBreak())
        # Doc. Custodia de Vehiculo  &  Convenio y Doc. Custodia Inmueble    y    Convenio y Doc. Custodia Vehiculo
        if((tipo_garantia=="Doc. Custodia de Vehiculo" and  len(deudores)>4) or (tipo_garantia=="Convenio y Doc. Custodia Inmueble" and  len(deudores)>4) or (tipo_garantia=="Convenio y Doc. Custodia Vehiculo" and  len(deudores)>4)):
            a=self._parrafos.append
            a(PageBreak()) 
        if(tipo_garantia=="Convenio" and len(deudores)==1):
            self._parrafos.append(Spacer(0,3))
        if(tipo_garantia == "Quirografaria"):
            a=self._parrafos.append
            a(PageBreak())
        if(tipo_garantia == "Convenio y Garantia personal" and len(deudores)>=5):
            a=self._parrafos.append
            a(PageBreak())
        texto= ('POR SI, COMO DEUDOR(A)(ES) o PRESTATARIO(A)(S):')
        self._parrafos.append(Paragraph(texto,style = estilos["Justify"]))        
        self._posicion_firmas(deudores)
        self._parrafos.append(Spacer(0,0.5*cm))
        if (len(fiadores) > 0):
            if((len(deudores)==2 and tipo_garantia=="Prendaria y Personal") or (tipo_garantia=="Personal y  Doc. custodia Vehiculo" and (len(deudores)==2))):
                a=self._parrafos.append
                a(PageBreak())
            if(len(deudores)+len(fiadores)==5 and (len(fiadores)==2 or len(fiadores)==1)):
                a=self._parrafos.append
                a(PageBreak())
            if(tipo_garantia=="Prendaria y Personal"):
                texto= ('Y COMO DEPOSITARIO(S) Y/O GARANTE(S) SOLIDARIO(A)(S), MANCOMUNADO(A)(S) E INDIVISIBLE(S): ')
            if(tipo_garantia!="Prendaria y Personal"):
                texto= ('Y COMO FIADOR(A)(ES) SOLIDARIO(A)(S), MANCOMUNADO(A)(S) E INDIVISIBLE(S): ')
            
            tipos_garantia_especiales = ["Quirografaria", "Convenio", "Doc. Custodia de Inmueble", 
                              "Doc. Custodia de Vehiculo", "Otros Doc. En Custodia", 
                              "Convenio y Doc. Custodia Inmueble", "Convenio y Doc. Custodia Vehiculo"]

            if tipo_garantia not in tipos_garantia_especiales:
                self._parrafos.append(Paragraph(texto,style = estilos["Justify"]))    
                self._posicion_firmas(fiadores)
                self._parrafos.append(Spacer(0,0.5*cm))
        # Doc. Custodia de Vehiculo    y    Convenio y Doc. Custodia Inmueble   y    Convenio y Doc. Custodia Vehiculo
        if((tipo_garantia=="Doc. Custodia de Vehiculo" and  2<len(deudores)<=4) or (tipo_garantia=="Convenio y Doc. Custodia Inmueble" and  2<len(deudores)<=4) or (tipo_garantia=="Convenio y Doc. Custodia Vehiculo" and  2<len(deudores)<=4)):
            a=self._parrafos.append
            a(PageBreak())
        # Otros Doc. En Custodia
        if(tipo_garantia=="Otros Doc. En Custodia" and  len(deudores)>4):
            a=self._parrafos.append
            a(PageBreak())
        # Otros Doc. En Custodia
        if((len(deudores)+len(fiadores))==2 and tipo_garantia=="Prendaria y Personal"):
            self._parrafos.append(Spacer(0,6))
        if((tipo_garantia=="Personal y  Doc. custodia Vehiculo" and (len(deudores)+len(fiadores))==2)):
            a=self._parrafos.append
            a(PageBreak())
        if((tipo_garantia=="Convenio y Garantia personal" and (len(deudores))==2) and (tipo_garantia=="Convenio y Garantia personal" and (len(fiadores))==2)):
            a=self._parrafos.append
            a(PageBreak())
        if(tipo_garantia=="Convenio y Garantia personal" and (len(deudores)+len(fiadores))==4 and (len(deudores)==3 or len(fiadores)==3)):
            self._parrafos.append(Spacer(0,4))
        texto= ('POR <b>GESTIÓN Y SOPORTE DE PROYECTOS JESÚS DEL GRAN PODER S.A.</b>')
        self._parrafos.append(Paragraph(texto,style = estilos["Justify"]))  
        self._parrafos.append(Spacer(0,2.3*cm))
        dato_nombre = self.nombreCompleto_repre()
        dato_cargo = self.__contrato["testimonio_poder"]["representante_legal"]["rol"]
        t_firmas=Table(
                    data=[[dato_nombre+'\n'+dato_cargo]],colWidths=8*cm,
                    style=[('ALIGN',(0,0),(-1,-1),'CENTER'),('FONT', (0,0), (-1,-1), 'Helvetica-Bold', tamanio_letra),])
        self._parrafos.append(t_firmas)

    def _posicion_firmas(self, dato):
        """
        Esta funcion posiciona las firmas
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        """ 
        for indice,item in enumerate(dato):
            if(indice!=len(dato)-1):
                if(indice%2==0):
                    self._parrafos.append(Spacer(0,2.3*cm))
                    dato_1=dato[indice]
                    dato_2=dato[indice+1]
                    t_firmas=Table(
                        data=[[dato_1['nombre_completo'].upper()+'\nC.I. N° '+dato_1['ci'], dato_2['nombre_completo'].upper()+'\nC.I. N° '+dato_2['ci']]],colWidths=8*cm,
                        style=[('ALIGN',(0,0),(-1,-1),'CENTER'),('FONT', (0,0), (-1,-1), 'Helvetica-Bold', tamanio_letra),])
                    self._parrafos.append(t_firmas)
            else:
                dato_1=dato[indice]
                if(len(dato)%2!=0):
                    self._parrafos.append(Spacer(0,2.3*cm))
                    t_firmas=Table(
                        data=[[dato_1['nombre_completo'].upper()+'\nC.I. N° '+dato_1['ci']]],colWidths=8*cm,
                        style=[('ALIGN',(0,0),(-1,-1),'CENTER'),('FONT', (0,0), (-1,-1), 'Helvetica-Bold', tamanio_letra)])
                    self._parrafos.append(t_firmas)
                else:
                    if(len(dato)==1):
                        self._parrafos.append(Spacer(0,2.3*cm))
                        t_firmas=Table(
                            data=[[dato_1[0]+'\nC.I. N° '+dato_1[1]]],colWidths=8*cm,
                            style=[('ALIGN',(0,0),(-1,-1),'CENTER'),('FONT', (0,0), (-1,-1), 'Helvetica-Bold', tamanio_letra)])
                        self._parrafos.append(t_firmas)
    
    def generar1(self):
        """
        Esta funcion crea un Bytes y almacena los datos
        Args:
            - self  : Un json (diccionario) y un usuario (string)
        Returns:
            BytesIO: debuelve el BytesIO en el cual se encuentran todos los datos
        """ 
        buffer = BytesIO()   
        documentos(buffer).build(self._parrafos, onFirstPage=self._encabezado,  onLaterPages=self._encabezado,canvasmaker=NumberedCanvas)
        return buffer
    