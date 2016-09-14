from GoogleSheetInterface import GoogleSheetInterface
import Utilities

class PotsSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1lDmx7291KyHrNtuw1CUMjrqU_mFfNjKtrWyjvwb8OBY'
    REAL_SPREADSHEET_ID = '10coSD2F22-iyHkrzmZqPCC2G41qYdO3PCzVe4RKEmLo'
    POTS_DATA_NAMED_RANGE = "PotsData"

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        
    def loadPotsData(self):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                            range=self.POTS_DATA_NAMED_RANGE).execute()
        return result
                  
    def getPotsList(self):
        potsList = []

        result = self.loadPotsData()
        potsData = result.get('values', [])
        
        if not potsData:
            print("There was a problem getting envelope data from the spreadsheet. It returned null.")
            return

        for i in range(0, len(potsData)):
            if (len(potsData[i]) > 0):
                potsList.append(potsData[i][0])
            
        return potsList