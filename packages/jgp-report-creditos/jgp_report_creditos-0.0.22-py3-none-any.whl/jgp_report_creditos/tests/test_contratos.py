import json
import requests
from jgp_report_creditos.report import makeContato

#API PARA EL TRABAJO

parametros ="301212612932"   
datos_json = requests.get("http://192.168.100.5:8000/api/v1/contratos/"+parametros).text
#Convenio y Garantia personal
datos_diccionario = json.loads(datos_json)
tipo_garantia=datos_diccionario["tipo_garantia"]["descripcion"]

# Nos creamos en la memoria
def write_bytesio_to_file(filename, bytesio):    
      """
      Esta funcion permite crear el pdf y lo guarda de manera local
      Args:
            - filename (string): el nombre del archivo del pdf que se creara
            - bytesio : Donde esta toda la información
      Returns:
            BytesIO: devuelve el BytesIO en el cual se encuentran todos los datos
      """
      with open(filename, "wb") as outfile:
            outfile.write(bytesio.getbuffer())
      bytesio.close()
      
# *********************************************************************************
#debe de aceptar cuando no envia nada o NOMBRE DEL LECTOR POR EJEMPLO (jtriguero)
# si no envia el parametro de usuario_x por defecto imprimira vacio
# *********************************************************************************
tipo_garantia=datos_diccionario["tipo_garantia"]["descripcion"]
parametros = datos_diccionario["codigo_operacion"]
usuario_x=""
# Llamada de funcion
buffer= makeContato(datos_diccionario, usuario_x)  
write_bytesio_to_file("Contrato "+tipo_garantia+" "+parametros+".pdf", buffer)
