class GoogleSheetsTable():
    mParentSpreadsheet = None
    mTableKeysColumn = ""
    mTableValuesColumn = ""
    mTableStartRow = -1
    mTableEndRow = -1
    mTableSheetName = ""
    #This variable will contain nothing until you load the data. Check its value.
    mTableKeys = None

    #tableValuesColumn2 allows you to have two values for every key. Value and Value2
    def __init__(self, parentSpreadsheet, tableKeysColumn, tableValuesColumn, tableStartRow, tableEndRow, tableSheetName, tableValuesColumn2 = None):
        self.mParentSpreadsheet = parentSpreadsheet
        self.mTableKeysColumn = tableKeysColumn
        self.mTableValuesColumn = tableValuesColumn
        self.mTableStartRow = tableStartRow
        self.mTableEndRow = tableEndRow
        self.mTableSheetName = tableSheetName
        #Note that mTableValuesColumn2 could be None. 
        self.mTableValuesColumn2 = tableValuesColumn2
        
    def getTableKeys(self):
        if (self.mTableKeys != None):
            return self.mTableKeys
        else:
            result = self.mParentSpreadsheet.getResultsSet(self.getTableKeysCellAddress())
            self.mTableKeys = result.get('values', [])
            return self.mTableKeys
    
    def getTableKeysCellAddress(self):
        address = "'" + self.mTableSheetName + "'!" 
        address = address + self.mTableKeysColumn + str(self.mTableStartRow) + ":"
        address = address + self.mTableKeysColumn + str(self.mTableEndRow)
        return address
        
    def addToTableRow(self, rowName, amountToAdd):
        tableKeys = self.getTableKeys()
        
        rowIndex = self.mTableStartRow
        foundRow = False
        #Find the pot row using the name
        for tableKey in tableKeys:
            if tableKey[0] == rowName:
                foundRow = True
                break
            
            rowIndex += 1
        
        if (foundRow == False):
            print("Couldn't find " + rowName + " in spreadsheet. TODO: throw error")
            return
            
        #Get the address for the cell, and add to it
        rowValueCellAddress = self.mParentSpreadsheet.getCellAddress(self.mTableSheetName, 
                                                                    self.mTableValuesColumn, rowIndex)
        self.mParentSpreadsheet.addToCell(rowValueCellAddress, amountToAdd)
    
    def getTableValue(self, key):
        tableKeys = self.getTableKeys()
        
        rowIndex = self.mTableStartRow
        foundRow = False
        #Find the pot row using the name
        for tableKey in tableKeys:
            if tableKey[0] == key:
                foundRow = True
                break
            
            rowIndex += 1
        
        if (foundRow == False):
            print("Couldn't find " + key + " in spreadsheet. TODO: throw error")
            return
            
        rowValueCellAddress = self.mParentSpreadsheet.getCellAddress(self.mTableSheetName, 
                                                                    self.mTableValuesColumn, rowIndex)
        return self.mParentSpreadsheet.getCellValue(rowValueCellAddress)
    
    def getTableValue2(self, key):
        if (self.mTableValuesColumn2 is None):
            print("Tables does not have a second value column. TODO: throw error")
            return None

        tableKeys = self.getTableKeys()
        
        rowIndex = self.mTableStartRow
        foundRow = False
        #Find the pot row using the name
        for tableKey in tableKeys:
            if tableKey[0] == key:
                foundRow = True
                break
            
            rowIndex += 1
        
        if (foundRow == False):
            print("Couldn't find " + key + " in spreadsheet. TODO: throw error")
            return
            
        rowValueCellAddress = self.mParentSpreadsheet.getCellAddress(self.mTableSheetName, 
                                                                    self.mTableValuesColumn2, rowIndex)
        return self.mParentSpreadsheet.getCellValue(rowValueCellAddress)
    
    def getKeysList(self):
        keysList = []

        tableKeys = self.getTableKeys()
        
        if not tableKeys:
            print("There was a problem getting keys from the spreadsheet. It returned null.")
            return

        for i in range(0, len(tableKeys)):
            if (len(tableKeys[i]) > 0):
                keysList.append(tableKeys[i][0])
            
        return keysList
