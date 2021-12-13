from socket import AddressFamily
from typing import ItemsView
import flask
import json
import os
from flask import request
import requests
from dataclasses import dataclass
from enum import Enum
from bs4 import BeautifulSoup
#----------------------------------------------------------------
#------------------------GOOGLE SHEET----------------------------
#----------------------------------------------------------------
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'webhoook-implementation-cebc-f06280d0e5b3.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.

# The ID spreadsheet.
SAMPLE_SPREADSHEET_ID = '1xUmoawsSSx7YYVRwJsGucnhDR8OmxZmhpyVMx2nlGJQ'

service = build('sheets', 'v4', credentials=credentials)
#----------------------------------------------------------------
#---------------------------FLASK--------------------------------
#----------------------------------------------------------------
#from forecast import Forecast, validate_params ## Esto seria un import para API
app = flask.Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return "Hello World"

# set FLASK_APP=flask_skeleton.py

# global name
# global lastname
# global id
# global Item
# global Address

@app.route('/webhook', methods=['POST', 'GET'])

def webhook():
    
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')
    print(action)

    if action == 'input.welcome':
        return {
                'fulfillmentText': (' Hola✨, (Nombre de la clienta).\nContamos con envíos gratis que dependen de tu código postal y con paquetes para comenzar tu propia Joyería de Acero Inoxidable. Déjanos los siguientes datos y con gusto te apoyaremos:\n\nIndicanos tu código postal')
                                        
            }  
      
    if action == 'input.GetZipCode':
        # Se ejecuta el input del insertar el zip.       
       return getzipcode(req)  
            
       
    if action == 'input.presupuesto':
        return presupuesto(req)

    if action == 'input.neworder':
        item = req.get('queryResult').get('parameters').get('item')
        
    if action == 'input.name':
        name = req.get('queryResult').get('parameters').get('name').get('name')
        print(name)
    if action == 'input.lastname':
        lastname = req.get('queryResult').get('parameters').get('last-name')  
        print(lastname)
    if action == 'input.id':
        id = req.get('queryResult').get('parameters').get('number')  
        print(id)    
    if action == 'input.address':
        address = req.get('queryResult').get('parameters').get('address')
        print(address)
        
        return {
            'fulfillmentText':f'Resumen de tus datos:\n\n Nombre completo:{name} {lastname}\n'
                              f'id:{id}\nAddress:{address}\nLote deseado:{item}\n\n'
                              f'¿Son correctos los datos?'
            }
    if action == 'Address.Address-yes':
        write2sheet_pending(item, name,lastname, id)
    


def getzipcode(req):
    
    # zipcode = req['queryResult']['parameters']['zip-code'] #### Esta manera tambien funciona pero creo que es mas lenta
    zipcode = req.get('queryResult').get('parameters').get('zip-code')
    url = 'http://zonasextendidas.com/consultarGuia.php'
    zipObj = {
        'numero': zipcode
    }
    zipResponse = requests.post(url, data = zipObj).text
    valores = zipResponse.split('=',1)

    dataObj = {
        'valores': valores[1]
    }
    dataResponse = json.loads(requests.get(url, params = dataObj).text)
    
    # Datos de envios----------------------------------------------------------------------------------
    # DHL
    try:
        freq_DHL = dataResponse['informacion']['DHL']['frecuencia'] # Frecuency (week days)
        ZE_DHL = dataResponse['informacion']['DHL']['zonaExtendida'] # Extended zone? 'Y' or '1' -> Yes / 'N' or '0' -> NO
        response_DHL =(f'DHL info:\nLUN - {"Yes" if freq_DHL[0] else "No"}, MAR - {"Yes" if freq_DHL[1] else "No"}, MIE - {"Yes" if freq_DHL[2] else "No"},'
                    f' JUE - {"Yes" if freq_DHL[3] else "No"}, VIE - {"Yes" if freq_DHL[4] else "No"}, SAB - {"Yes" if freq_DHL[5] else "No"}\n'
                    f'Extended Zone -> {"YES" if ZE_DHL=="1" or ZE_DHL =="Y" else "NO"}\n')
    except:
        response_DHL =(f'DHL no hace envios a ese codigo postal!\n')
    # Fedex
    try:
        express_Fedex = dataResponse['informacion']['Fedex']['express'] # Express delivery ('1' -> YES / '0' -> NO)
        ground_Fedex = dataResponse['informacion']['Fedex']['terrestre'] # Ground delivery ('1' -> YES / '0' -> NO)
        ZE_Fedex = dataResponse['informacion']['Fedex']['zonaExtendida'] # Extended zone? 'Y' or '1' -> Yes / 'N' or '0' -> NO
        response_Fedex = (f'Fedex info:\nExpress delivery -> {"YES" if express_Fedex =="1" else "NO"}\nGround delivery -> {"YES" if ground_Fedex =="1" else "NO"}\n'
                        f'Extended Zone -> {"YES" if ZE_Fedex =="1" or ZE_Fedex =="Y" else "NO"}\n')  
    except:
        response_Fedex =(f'Fedex no hace envios a ese codigo postal!\n')
    # Estafeta
    try:
        Info_Estafeta = dataResponse['informacion']['Estafeta'] # Frecuency (week days)
        keys = ("lunes","martes","miercoles","jueves","viernes","sabado")
        freq_Estafeta = list(Info_Estafeta.get(key) for key in keys)
        ZE_Estafeta = dataResponse['informacion']['Estafeta']['zonaExtendida'] # Extended zone? 'Y' or '1' -> Yes / 'N' or '0' -> NO
        response_Estafeta = (f'Estafeta info:\nLUN - {"Yes" if freq_Estafeta[0] =="1" else "No"}, MAR - {"Yes" if freq_Estafeta[1] =="1" else "No"}, MIE - {"Yes" if freq_Estafeta[2] =="1" else "No"},'
                    f' JUE - {"Yes" if freq_Estafeta[3] =="1" else "No"}, VIE - {"Yes" if freq_Estafeta[4] =="1" else "No"}, SAB - {"Yes" if freq_Estafeta[5] =="1" else "No"}\n'
                    f'Extended Zone -> {"YES" if ZE_Estafeta=="1" or ZE_Estafeta =="Y" else "NO"}\n')
    except:
        response_Estafeta =(f'Estafeta no hace envios a ese codigo postal!\n')
    # RedPack
    try:
        ZE_RedPack = dataResponse['informacion']['RedPack']['zonaExtendida'] # Extended zone? 'Y' or '1' -> Yes / 'N' or '0' -> NO
        response_RedPack = (f'RedPack info:\nExtended Zone -> {"YES" if ZE_RedPack=="1" or ZE_RedPack=="Y"else "NO"}')
    except:
        response_RedPack =(f'RedPack no hace envios a ese codigo postal!\n')
    #--------------------------------------------------------------------------------------------------

    return {
        'fulfillmentText':f'Your zip code is: {zipcode}\nEspera mientras verificamos tu codigo postal\n'
                        f'------------------------------------------------------------------------------------------\n'                               
                        f'Deliveries INFO:\n\n{response_DHL}\n{response_Fedex}\n{response_Estafeta}\n{response_RedPack}\n\n'
                        f'Por favor, indica el presupuesto del que dispones en dolares'
                        
    }                    

def presupuesto(req):
    
    presupuesto = req.get('queryResult').get('parameters').get('presupuesto').get('amount')
    presupuesto = float(presupuesto)
    url = 'https://www.joyeriasanchez.com/16-pendientes'
    data = requests.get(url)
    soup = BeautifulSoup(data.content, 'lxml')
    divs = soup.find('div', {'class': 'product_list'})
    children = divs.find_all('div',{'class': 'ajax_block_product'})
    output = ''
    for child in children:
        try:
            image_link = child.find('img', {'class':'img-responsive'}).get('src')
            title = child.find('p',{'class':'product-desc'}).text
            price = child.find('span', {'class':'price product-price'}).text
            price = float((price.split(' ')[1]).replace(',','.'))
                    
            if price <= presupuesto:
               a =  f'{image_link}\n{title}\n{price}$\n' 
               output = f'{output}{a}'
        except:
            pass
    # a = 'https://www.joyeriasanchez.com/45398-home_default/pendientes-viceroy-plata-mujer-corazon-circonitas-7112e000-38.jpg'
    return{
        'fulfillmentText':  f'{output}\n\nSelecciona el lote que deseas'
    }     

def write2sheet_pending(item, name,lastname, id, address):
    body = [['pedido nuevo',item, name, lastname,id, address,'NO PAGADO','EN TRAMITACION']]
    request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1", 
                            valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":body})
    response = request.execute()

if __name__ == "__main__":
    app.secret_key = 'ItIsASecret'
    app.debug = True
    app.run()