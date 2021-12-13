
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

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Pedidos!A:G").execute()
values = result.get('values', [])
print(values) #lista de listas
# body = [n pedido,DNI,Nombre,Apellido,Direccion,Estado Pago,Estado del pedido]
body = [["56", "89374899","Jasan","Ramitriv","Potato Street 4-7D","PAGADO","ENTREGADO"]]
request = service.spreadsheets().values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="A1", 
                            valueInputOption="USER_ENTERED", insertDataOption="INSERT_ROWS", body={"values":body})
response = request.execute()
print(response)