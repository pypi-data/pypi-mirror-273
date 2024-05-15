import json
from reportlab.platypus import (SimpleDocTemplate, Spacer, Paragraph, Table)

import datetime
import io
#from msilib import Table

import os
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

#preubas 2 round
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle

#
import requests
from reportlab.lib.pagesizes import letter
import os
# Importaciones para la tabla
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT

class Componets:
    index=1
    cont=1
    def __init__(self, canvas):
        self.canvas = canvas

    def DrawRectanguleBorder(self, text_label, text,x, y, pwidth, tamaño_label): 
        """
        Dibuja el rectangulo con su respectivo label 
        Args:
            - self : Un canvas (canvas)
            - text_label (string): el texto que ira de manera estatica
            - text (string): el texto que ira dentro del rectangulo
            - x (double): la posicion en el eje x
            - y (double): la posicion en el eje y
            - pwidth (double): El tamaño total del objeto  ancho
            - tamaño_label (double): El tamaño que ocupara el label estatico
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        pheight =0.5 # tamaño_label
        y= y-pheight
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            y=25.71- pheight
            
        label_sm = tamaño_label     # *cm  tamaño: lable_smedio 2cm
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text_label)
        # Dibujar el rectángulo rect(self, x, y, width, height, stroke=1, fill=0)
        self.canvas.setLineWidth(0.4)# grosor de la linea
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.setFillColor(colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255)))
        self.canvas.rect((x+label_sm)*cm, y*cm, (pwidth-label_sm)*cm, (pheight-0.1)*cm, stroke = 1,fill=1)# borde
        # Agregar el texto dentro del rectángulo
        self.canvas.setFont("Helvetica", 8)
        self.canvas.setFillColor(colors.black)
        #pwidth-tamaño_label
        lineas = []
        if(text!="" and text!=None ):
            palabras = text.split() 
            linea_actual = palabras[0] 
            for palabra in palabras[1:]: 
                if self.canvas.stringWidth(linea_actual + " " + palabra, "Helvetica", 8) <= (pwidth-tamaño_label)*cm: 
                    linea_actual += " " + palabra 
                else: 
                    lineas.append(linea_actual) 
                    linea_actual = palabra 
            lineas.append(linea_actual) 
            text=lineas[0]
            estilos = getSampleStyleSheet()
            font_size=8
            estilos.add(ParagraphStyle(name='texto_into_box', alignment=TA_LEFT, fontSize=font_size, fontName='Helvetica',leading=8,textColor=colors.black))
            estilo_titulo = estilos["texto_into_box"]
            parrafo = Paragraph(text, estilo_titulo)
            parrafo.wrapOn(self.canvas, (pwidth-tamaño_label-0.2) * cm, 0.5 * cm)  # Anchura y altura máxima del párrafo en puntos
            parrafo.drawOn(self.canvas, (x+label_sm+0.2)*cm, (y + 0.1) * cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
        else:
            estilos = getSampleStyleSheet()
            font_size=8
            estilos.add(ParagraphStyle(name='cadena_vacia', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica',leading=8,textColor=colors.black))
            estilo_titulo = estilos["cadena_vacia"]
            text="-"
            parrafo = Paragraph(text, estilo_titulo)
            parrafo.wrapOn(self.canvas, (pwidth-tamaño_label) * cm, 0.5 * cm)  # Anchura y altura máxima del párrafo en puntos
            parrafo.drawOn(self.canvas, (x+label_sm)*cm, (y + 0.15) * cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
        return y
                
    def DrawPalabra(self, text,x, y):
        """
        Dibuja un texto en las posiciones dadas siendo x=absisas y=ordenadas
        Args:
            - self : Un canvas (canvas)
            - text (string): el texto que se colora
            - x (double): la posicion en el eje x
            - y (double): la posicion en el eje y
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        #tamaño_label eje y
        pheight =0.5   # *cm estatico
        y= y-pheight
        if(y<2):            
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            y=25.71- pheight        
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text)
        return y

    def draw_line_gruesa_subtitulo(self, y, subtitulo): 
        """
        Dibuja una linea gruesa con su respectivo subtitulo
        Args:
            - self : Un canvas (canvas)
            - subtitulo (string): el texto que ira como subtitulo para separar una nueva seccion
            - y (double): la posicion en el eje y
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        # line 
        ancho, alto = letter
        pheight=0.4
        y= y-pheight
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo,self.index,40)
            y=25.71
        self.canvas.setLineWidth(2)# grosor de la linea
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, y*cm, ancho-30.9, y*cm)
        # Agregar el subtitulo
        self.canvas.setFillColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.setFont("Helvetica-Bold", 8)
        self.canvas.drawString(2 * cm, (y-0.4)* cm, subtitulo)
        return y-0.5

    def DrawCheckBox(self, text_label, x, y, pwidth, tamaño_label, sw):
        """
        Dibuja el rectangulo con un check, asi tambien el texto o label que lo representa. 
        Args:
            - self : Un canvas (canvas)
            - text_label (string): el texto que ira de manera estatica
            - text (string): el texto que ira dentro del rectangulo
            - x (double): la posicion en el eje x
            - y (double): la posicion en el eje y
            - pwidth (double): el tamaño total del objeto  ancho
            - tamaño_label (double): el tamaño que ocupara el label estatico
            - sw (bool): si es True se coloca el check y si es False no se coloca nada dentro del rectangulo
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        #tamaño_label
        pheight =0.5   # *cm estatico
        y= y-pheight
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo)
            y=25.71- pheight
        label_sm = tamaño_label     #*cm  tamaño: lable_smedio 2cm
        # Agregar el texto label
        self.canvas.setFillColor(colors.black)
        self.canvas.setFont("Helvetica", 8)
        self.canvas.drawString(x * cm, (y+0.1)* cm, text_label)
        # Dibujar el rectángulo rect(self, x, y, width, height, stroke=1, fill=0)
        self.canvas.setLineWidth(0.4)# grosor de la linea
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.setFillColor(colors.Color(red=(221.0/255),green=(221.0/255),blue=(221.0/255)))
        self.canvas.rect((x+label_sm)*cm, y*cm, (pwidth-label_sm)*cm, (pheight-0.1)*cm, stroke = 1,fill=1)# borde
        if sw:
            pheight_check=0.45 # Agregar simbolo check si lo requiere
            self.canvas.setFont("Helvetica", pheight_check*cm) # Dibujar el símbolo de marca de verificación
            self.canvas.setFillColor(colors.black)
            self.canvas.drawString((x+label_sm+0.1)*cm, (y + 0.05) * cm, u"\u2713")  # Código Unicode para el símbolo de marca de verificación
        return y

    def TableSign(self,x,y):
        """
        Dibuja una tabla para las firmas con valores estaticos
        Args:
            - x (double): la posicion en el eje x
            - y (double): la posicion en el eje y
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        # Agregar la cabecera de la tabla   
        table = [["", "", ""],
                ["FIRMA DEL CLIENTE", "FIRMA Y SELLO DE ASESOR COMERCIAL", "FIRMA Y SELLO PLATAFORMA"]]
        # Definir el tamaño de cada columna
        col_widths = [6.2*cm, 6.2*cm, 6.2*cm]
        row_widths = [1.6*cm, 0.4*cm]
        # Definir el estilo de la tabla
        style = TableStyle([           
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),# interlineado Puede ser TOP, MIDDLE o BOTTOM
            ('GRID', (0, 0), (-1, -1), 0.5, colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))),#color de la tabla(lineas)
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))),# color del subtitulo
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('ALIGN',(0, 0), (-1, -1),'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ])
        # Crear la tabla
        table = Table(table, colWidths=col_widths, rowHeights=row_widths)
        # Aplicar el estilo a la tabla
        table.setStyle(style)
        # Dibujar la tabla en el lienzo
        table.wrapOn(self.canvas, 20, 10)
        # Posición de la tabla "lienzo" (x,y)
        table.drawOn(self.canvas, x*cm, (y-2.5+0.35)*cm)# 2.5 ancho de la tabla
        return y-2.5+0.3
    
    #excelente
    def Paragraph(self,x, y, texto, width, height):
        """
        Dibuja un parrafo largo en un determinado ancho, alto , posicion "x" y posicion "y" 
        Args:
            - self : Un canvas (canvas)
            - x (double): la posicion en el eje x
            - y (double): la posicion en el eje y
            - texto (string): el parrafo que se debe de colocar
            - pwidth (double): el tamaño total del objeto ancho
            - pheight (double): el tamaño total del objeto alto
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        y=(y-0.3-height)
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='parrafo', alignment=TA_JUSTIFY, fontSize=6, fontName='Helvetica',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        estilo_titulo = estilos["parrafo"]
        parrafo = Paragraph(texto, estilo_titulo)
        parrafo.wrapOn(self.canvas, width*cm, height*cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(self.canvas, x * cm, y* cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
        return (y)
    # bien
    def draw_line_delgada(self,y): 
        """
        Dibuja una linea delgada y la posiciona en el eje y dado
        Args:
            - self : Un canvas (canvas)
            - y (double): la posicion en el eje y
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        # linea
        tobutton=0.2
        ancho, alto = letter
        self.canvas.setLineWidth(0.8)# grosor de la linea
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, (y-tobutton)*cm, ancho-30.9, (y-tobutton)*cm)
        return y-0.3

    #  excelente
    def draw_line_delgada_con_label(self, y, subtitulo): 
        """
        Dibuja una linea delgada y la posiciona en el eje "y" dado, asi tambien coloca un subtitulo
        Args:
            - self : Un canvas (canvas)
            - y (double): la pocision en el eje y
            - subtitulo (string): 
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        """ line """
        ancho, alto = letter
        pheight=0.2
        y = y-pheight
        if(y<2):
            self.canvas.showPage()
            titulo="DEPOSITOS EN BANCO"
            self.index=self.index+1
            self.encabezado(titulo,self.index,40)
            y=25.71
        self.canvas.setLineWidth(0.8)# grosor de la linea
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, y*cm, ancho-30.9, y*cm)
        # Agregar el subtitulo
        self.canvas.setFillColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.setFont("Helvetica-Bold", 8)
        self.canvas.drawString(2 * cm, (y-0.4)* cm, subtitulo)
        return y-0.5

    def ajustar_fuente_para_wrap(self,texto, estilo, ancho_maximo):
        """
        Sirve para ajustar la fuente del texto
        Args:
            - self : Un canvas (canvas)
            - texto (string): el texto o parrafo a ser modificado segun el ancho dado
            - estilo (string): es el estilo de letra que tiene el texto o parrafo
            - ancho_maximo (double): es al ancho que no debe de sobre pasar
        """
        from reportlab.pdfbase.pdfmetrics import stringWidth, getFont
        fuente = getFont(estilo.fontName)
        tamaño_inicial = estilo.fontSize
        ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        while ancho_texto > ancho_maximo and tamaño_inicial > 1:
            tamaño_inicial -= 1
            ancho_texto = stringWidth(texto, estilo.fontName, tamaño_inicial)
        estilo.fontSize = tamaño_inicial

    def encabezado(self,titulo, usuario):
        """
        Coloca el encabezado de pagina con los datos correspondientes.
        Args:
            - self : Un canvas (canvas)
            - titulo (string): el titulo que corresponde al reporte
            - usuario (string): es el usuario que se loguea en el sistema
        Returns:
            double: la pocision en la cual se coloco la ultima modificacion
        """
        # Encabezado
        self.canvas.setFont('Helvetica',7) # corregido
        x= datetime.datetime.now() # obtengo la fecha actual
        ancho, alto = letter
        formatoFecha= x.strftime("%d/%m/%Y")
        self.canvas.drawString(ancho-90, 27*cm, 'Fecha: '+formatoFecha)
        self.canvas.drawString(ancho-90, 26.6*cm, usuario)
        # Titulo 
        estilos = getSampleStyleSheet()
        font_size=14
        estilos.add(ParagraphStyle(name='titulo', alignment=TA_CENTER, fontSize=font_size, fontName='Helvetica-Bold',leading=8,textColor=colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255))))
        ancho, alto=letter
        estilo_titulo = estilos["titulo"]
        self.ajustar_fuente_para_wrap(titulo, estilo_titulo, 10.8 * cm)
        parrafo = Paragraph(titulo, estilo_titulo)
        parrafo.wrapOn(self.canvas, 9.5 * cm, 1 * cm)  # Anchura y altura máxima del párrafo en puntos
        parrafo.drawOn(self.canvas, 8 *cm, 27*cm)  # Coordenadas (x, y) de la esquina superior izquierda del párrafo
        # imagen
        img = os.path.join(os.path.dirname(os.path.abspath(__file__)),'../resources/img/logo_jgp.png')
        # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
        self.canvas.drawImage(img, 2 * cm, 26.1 * cm, 160, 35, mask=None)  
        # line 
        ancho, alto = letter
        self.canvas.setLineWidth(2)
        self.canvas.setLineCap(1)  # Extremo redondeado. (0) Default: Cuadrado Sin Proyección
        self.canvas.setStrokeColor(colors.Color(red=(23.0/255),green=(25.0/255),blue=(50.0/255)))
        self.canvas.line(2*cm, 25.7*cm, ancho-30.9, 25.7*cm)
        return 25.7 #0.3 espacio de abajo