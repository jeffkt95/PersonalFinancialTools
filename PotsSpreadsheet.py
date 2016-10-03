from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable

class PotsSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1lDmx7291KyHrNtuw1CUMjrqU_mFfNjKtrWyjvwb8OBY'
    REAL_SPREADSHEET_ID = '10coSD2F22-iyHkrzmZqPCC2G41qYdO3PCzVe4RKEmLo'
    SHEET_NAME = "Savings Pots"
    #Cell where the savings total is
    TOTAL_CELL = "B11"
    
    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        self.mPotsTable = GoogleSheetsTable(self, "A", "B", 12, 33, self.SHEET_NAME)

    def getPotsTable(self):
        return self.mPotsTable
        
    def copyPasteShiftPreviousPots(self):
        self.insertColumn(1, self.SHEET_NAME)
        self.copyPasteColumn(self.SHEET_NAME, 2, 1)
        #TODO: Set date in row 1 to today's date, and clear the note in the bottom row
        
    def addToTotal(self, amountToAdd):
        totalCellAddress = "'" + self.SHEET_NAME + "'!" + self.TOTAL_CELL
        self.addToCell(totalCellAddress, amountToAdd)
