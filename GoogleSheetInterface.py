import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

#TODO: conside making a more generic class for connecting to any google spreadsheet. Then sub-class it for the Envelopes functionality.
#Right now it's got no Envelopes specific stuff (except for the spreadsheet ID), so it would be easiest to do that FIRST, 
#before you soil it.
class GoogleSheetInterface:
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        print("Hello world")
        
    def connect(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        
    #Gets the value of a single cell
    #Cell address is of the form "<column letter><row number>", e.g. "A5"
    def getCellValue(self, sheetName, cellAddress):
        fullCellAddress = sheetName + "!" + cellAddress
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=fullCellAddress).execute()
        values = result.get('values', [])
        return values[0][0]

    def setCellValue(self, sheetName, cellAddress, value):
        fullCellAddress = sheetName + "!" + cellAddress
        myBody = {u'range': fullCellAddress, u'values': [[str(value)]], u'majorDimension': u'ROWS'}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=fullCellAddress, body=myBody, valueInputOption='USER_ENTERED').execute()
    
    
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
