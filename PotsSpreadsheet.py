from GoogleSheetInterface import GoogleSheetInterface
import Utilities

class PotsSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1lDmx7291KyHrNtuw1CUMjrqU_mFfNjKtrWyjvwb8OBY'
    REAL_SPREADSHEET_ID = '10coSD2F22-iyHkrzmZqPCC2G41qYdO3PCzVe4RKEmLo'
    #POTS_DATA_NAMED_RANGE = "PotsData"
    
    mTableKeyColumn = "A"
    mTableValueColumn = "B"
    mTableStartRow = 12
    mTableEndRow = 33
    mTableSheetName = "Savings Pots"
    #This variable will contain nothing until you load the data. Check it's value.
    mTableKeys = None

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        
    def getPotsKeys(self):
        if (self.mTableKeys != None):
            return self.mTableKeys
        else:
            result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                                range=self.getTableKeysCellAddress()).execute()
            self.mTableKeys = result.get('values', [])
            return self.mTableKeys
    
    def getTableKeysCellAddress(self):
        address = "'" + self.mTableSheetName + "'!" 
        address = address + self.mTableKeyColumn + str(self.mTableStartRow) + ":"
        address = address + self.mTableKeyColumn + str(self.mTableEndRow)
        return address
        
    def addToPot(self, potName, amountToAdd):
        tableKeys = self.getPotsKeys()
        
        rowIndex = self.mTableStartRow
        foundPot = False
        #Find the pot row using the name
        for tableKey in tableKeys:
            print("Checking if " + tableKey[0] + " is the same as " + str(potName))
            if tableKey[0] == potName:
                foundPot = True
                break
            
            rowIndex += 1
        
        if (foundPot == False):
            print("Couldn't find " + potName + " in spreadsheet. TODO: throw error")
            return
            
        #Get the value
        potValueCellAddress = self.getCellAddress(self.mTableSheetName, self.mTableValueColumn, rowIndex)
        originalPotValue = self.getCellValue(potValueCellAddress)
        
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
        self.setCellValue(potValueCellAddress, str(newPotValue))
        
    def getPotsList(self):
        potsList = []

        potsKeys = self.getPotsKeys()
        
        if not potsKeys:
            print("There was a problem getting pots data from the spreadsheet. It returned null.")
            return

        for i in range(0, len(potsKeys)):
            if (len(potsKeys[i]) > 0):
                potsList.append(potsKeys[i][0])
            
        return potsList
