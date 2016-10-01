from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable

class PotsSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1lDmx7291KyHrNtuw1CUMjrqU_mFfNjKtrWyjvwb8OBY'
    REAL_SPREADSHEET_ID = '10coSD2F22-iyHkrzmZqPCC2G41qYdO3PCzVe4RKEmLo'
    
    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        self.mPotsTable = GoogleSheetsTable(self, "A", "B", 12, 33, "Savings Pots")

    def getPotsTable(self):
        return self.mPotsTable