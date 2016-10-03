import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import webbrowser
import Utilities


class GoogleSheetInterface:
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    SCOPES = 'https://www.googleapis.com/auth/drive'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'
    SPREADSHEET_URL_ROOT = 'https://docs.google.com/spreadsheets/d/'

    def __init__(self, spreadsheetId):
        self.spreadsheetId = spreadsheetId
        
    def connect(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                  discoveryServiceUrl=discoveryUrl)
        
    def getResultsSet(self, queryRange):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                            range=queryRange).execute()
        return result
            
    #Gets the value of a single cell
    #If sheetName is None, the assumption is it's already embedded in the cell address. If not, then the code will concatentate
    #sheetName and cellAddress to get the full cell address.
    def getCellValue(self, cellAddress, sheetName = None):
        if (sheetName is not None):
            cellAddress = sheetName + "!" + cellAddress
            
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=cellAddress).execute()
        values = result.get('values', [])
        if (len(values) < 1):
            return None
        else:
            return values[0][0]

    def getCellAddress(self, sheetName, column, row):
        address = "'" + sheetName + "'!"
        address = address + column + str(row)
        return address

    #Gets the value of a single cell with a named range
    def getCellValueNamedRange(self, namedRange):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, range=namedRange).execute()
        values = result.get('values', [])
        return values[0][0]

    #Open up this spreadsheet in a web browser.
    def openSpreadsheet(self):
        spreadsheetUrl = self.SPREADSHEET_URL_ROOT + self.spreadsheetId
        webbrowser.open(spreadsheetUrl)
        
    #Sets the value of a single cell
    #If sheetName is None, the assumption is its already embedded in the cell address. If not, then the code will concatentate
    #sheetName and cellAddress to get the full cell address.
    def setCellValue(self, cellAddress, value, sheetName = None):
        if (sheetName is not None):
            cellAddress = sheetName + "!" + cellAddress

        myBody = {u'range': cellAddress, u'values': [[str(value)]], u'majorDimension': u'ROWS'}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=cellAddress, body=myBody, valueInputOption='USER_ENTERED').execute()
    
    def copyPasteColumn(self, worksheetName, sourceColumn, destinationColumn):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'copyPaste': {
                u'source': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(0),
                    u'startColumnIndex': str(sourceColumn),
                    u'endColumnIndex': str(sourceColumn + 1)
                },
                u'destination': {
                    u'sheetId': str(worksheetId),
                    u'startRowIndex': str(0),       #Leave out endRowIndex to include all rows
                    u'startColumnIndex': str(destinationColumn),
                    u'endColumnIndex': str(destinationColumn + 1)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()
    
    def insertColumn(self, columnIndex, worksheetName):
        worksheetId = self.getWorksheetIdByName(worksheetName)
        
        myBody = {u'requests': [
        {
            u'insertDimension': {
                u'range': {
                    u'sheetId': str(worksheetId),
                    u'dimension': u'COLUMNS',
                    u'startIndex': str(columnIndex),
                    u'endIndex': str(columnIndex + 1)
                }
            }
        }
        ]}

        self.service.spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheetId, body=myBody).execute()
        
    def addToCell(self, cellAddress, amountToAdd):
        originalPotValue = self.getCellValue(cellAddress)
        
        if (originalPotValue == None):
            originalPotValue = 0
        
        if (Utilities.is_number(originalPotValue) == False):
            originalPotValue = Utilities.getNumber(originalPotValue)
        else:
            originalPotValue = float(originalPotValue)
        
        if (Utilities.is_number(amountToAdd) == False):
            amountToAdd = Utilities.getNumber(amountToAdd)
        else:
            amountToAdd = float(amountToAdd)
                    
        #Set the value to the retrieved value plus the amountToAdd
        newPotValue = originalPotValue + amountToAdd
        self.setCellValue(cellAddress, str(newPotValue))
    
    def getWorksheetIdByName(self, worksheetName):
        # https://developers.google.com/sheets/samples/sheet#determine_sheet_id_and_other_properties
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId, fields='sheets.properties').execute()
        
        sheets = result.get('sheets', [])

        for sheetProperties in sheets:
            theProperties = sheetProperties.get('properties')
            title = theProperties.get('title')
            if title == worksheetName:
                return theProperties.get('sheetId')

        print("TODO: Need to throw error. '" + worksheetName + "' sheet not found.")
        return -1
    
    def getNumRowsInWorksheet(self, worksheetName):
        # https://developers.google.com/sheets/samples/sheet#determine_sheet_id_and_other_properties
        result = self.service.spreadsheets().get(spreadsheetId=self.spreadsheetId, fields='sheets.properties').execute()
        
        sheets = result.get('sheets', [])

        for sheetProperties in sheets:
            theProperties = sheetProperties.get('properties')
            title = theProperties.get('title')
            if title == worksheetName:
                gridProperties = theProperties.get('gridProperties')
                rowCount = gridProperties.get('rowCount')
                return rowCount

        print("TODO: Need to throw error. '" + worksheetName + "' sheet not found.")
        return -1
    
    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        flags = None
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'sheets.googleapis.com-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            #if flags:
            credentials = tools.run_flow(flow, store, flags)
            #else: # Needed only for compatibility with Python 2.6
            #    credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
