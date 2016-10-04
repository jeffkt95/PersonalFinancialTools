import unittest
from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetInterface import SheetNotFoundError
import Utilities
from googleapiclient.errors import HttpError

class TestGoogleSheetInterface(unittest.TestCase):
    UNIT_TEST_SPREADSHEET_ID = "1DVuL4Pf5KfblavC8X92p62oCU_cTxgfUBWloQcwsmsE"
    FIRST_SHEET_NAME = "My first sheet"
    SECOND_SHEET_NAME = "My second sheet"
    THIRD_SHEET_NAME = "My third sheet"
    BAD_SHEET_NAME = "Non-existent sheet name"
    NAMED_RANGE = "MyNamedCell"
    BAD_NAMED_RANGE = "Non-existent named range"

    def setUp(self):
        self.googleSheet = GoogleSheetInterface(self.UNIT_TEST_SPREADSHEET_ID)
        self.googleSheet.connect()
    
    #def tearDown(self):
        #Nothing to do
        
    def test_getCellValue(self):
        #Test method with sheet name provided separately
        cellValue = self.googleSheet.getCellValue("A1", self.FIRST_SHEET_NAME)
        self.assertEqual(Utilities.getNumber(cellValue), 10.0)
        
        #Test method with sheet name concatentated with 
        cellValue = self.googleSheet.getCellValue(self.FIRST_SHEET_NAME + "!A1")
        self.assertEqual(Utilities.getNumber(cellValue), 10.0)
        
        #Test bad sheet name
        with self.assertRaises(HttpError):
            cellValue = self.googleSheet.getCellValue("A1", self.BAD_SHEET_NAME)

        #Test bad cell address
        with self.assertRaises(HttpError):
            cellValue = self.googleSheet.getCellValue("YourMom", self.FIRST_SHEET_NAME)
        
    def test_getCellAddress(self):
        cellAddress = self.googleSheet.getCellAddress("MySheetName", "D", 10)
        self.assertEqual(cellAddress, "'MySheetName'!D10")
        
    def test_getCellValueNamedRange(self):
        cellValue = self.googleSheet.getCellValueNamedRange(self.NAMED_RANGE)
        self.assertEqual(20, Utilities.getNumber(cellValue))
        
        #Test non-existent named range
        with self.assertRaises(HttpError):
            cellValue = self.googleSheet.getCellValueNamedRange(self.BAD_NAMED_RANGE)
            
    def test_setCellValue(self):
        #First check that the value is different before
        cellValueBefore = self.googleSheet.getCellValue("A3", self.FIRST_SHEET_NAME)
        self.assertEqual(30, Utilities.getNumber(cellValueBefore))
        
        #Set it, then check that it took the change
        self.googleSheet.setCellValue("A3", 35, self.FIRST_SHEET_NAME)
        cellValueAfter = self.googleSheet.getCellValue("A3", self.FIRST_SHEET_NAME)
        self.assertEqual(35, Utilities.getNumber(cellValueAfter))
        
        #Finally, set it back to what it was before you started
        self.googleSheet.setCellValue("A3", 30, self.FIRST_SHEET_NAME)
        cellValueFinally = self.googleSheet.getCellValue("A3", self.FIRST_SHEET_NAME)
        self.assertEqual(30, Utilities.getNumber(cellValueFinally))
        
    def test_copyPasteColumn(self):
        self.googleSheet.copyPasteColumn(self.THIRD_SHEET_NAME, 0, 1)
        numRows = self.googleSheet.getNumRowsInWorksheet(self.THIRD_SHEET_NAME)
        
        for i in range(1, numRows):
            firstColumnCellAddress = self.googleSheet.getCellAddress(self.THIRD_SHEET_NAME, "A", i)
            secondColumnCellAddress = self.googleSheet.getCellAddress(self.THIRD_SHEET_NAME, "B", i)
            firstColumnValue = self.googleSheet.getCellValue(firstColumnCellAddress)
            secondColumnValue = self.googleSheet.getCellValue(secondColumnCellAddress)
            self.assertEqual(firstColumnValue, secondColumnValue)
            
        #Delete the column and insert it back in so it's ready for next time
        self.googleSheet.deleteColumn(1, self.THIRD_SHEET_NAME)
        self.googleSheet.insertColumn(1, self.THIRD_SHEET_NAME)
        
        
    def test_insertDeleteColumn(self):
        #First check the values before the insert
        cellBeforeInsert = self.googleSheet.getCellValue("A1", self.SECOND_SHEET_NAME)
        cellAfterInsert = self.googleSheet.getCellValue("B1", self.SECOND_SHEET_NAME)
        self.assertEqual("Column before insert", cellBeforeInsert)
        self.assertEqual("Column after insert", cellAfterInsert)
        
        #Next insert the column and check the values
        self.googleSheet.insertColumn(1, self.SECOND_SHEET_NAME)
        cellBeforeInsert = self.googleSheet.getCellValue("A1", self.SECOND_SHEET_NAME)
        cellInserted = self.googleSheet.getCellValue("B1", self.SECOND_SHEET_NAME)
        cellAfterInsert = self.googleSheet.getCellValue("C1", self.SECOND_SHEET_NAME)
        self.assertEqual("Column before insert", cellBeforeInsert)
        self.assertEqual(None, cellInserted)
        self.assertEqual("Column after insert", cellAfterInsert)
        
        #Finally delete the column and check that it's back to how it started
        self.googleSheet.deleteColumn(1, self.SECOND_SHEET_NAME)
        cellBeforeInsert = self.googleSheet.getCellValue("A1", self.SECOND_SHEET_NAME)
        cellAfterInsert = self.googleSheet.getCellValue("B1", self.SECOND_SHEET_NAME)
        self.assertEqual("Column before insert", cellBeforeInsert)
        self.assertEqual("Column after insert", cellAfterInsert)
          
    def test_addToCell(self):
        cellValueBefore = self.googleSheet.getCellValue("A4", self.FIRST_SHEET_NAME)
        self.assertEqual(40, Utilities.getNumber(cellValueBefore))
        
        #Set it, then check that it took the change
        self.googleSheet.addToCell("'" + self.FIRST_SHEET_NAME + "'!A4", 5)
        cellValueAfter = self.googleSheet.getCellValue("A4", self.FIRST_SHEET_NAME)
        self.assertEqual(45, Utilities.getNumber(cellValueAfter))
        
        #Finally, set it back to what it was before you started
        self.googleSheet.setCellValue("A4", 40, self.FIRST_SHEET_NAME)
        cellValueFinally = self.googleSheet.getCellValue("A4", self.FIRST_SHEET_NAME)
        self.assertEqual(40, Utilities.getNumber(cellValueFinally))
        
    def test_getWorksheetIdByName(self):
        firstWorksheetId = self.googleSheet.getWorksheetIdByName(self.FIRST_SHEET_NAME)
        self.assertEqual(0, firstWorksheetId)
        
        secondWorksheetId = self.googleSheet.getWorksheetIdByName(self.SECOND_SHEET_NAME)
        self.assertEqual(830853517, secondWorksheetId)

        #Test where worksheet is not found
        with self.assertRaises(SheetNotFoundError):
            self.googleSheet.getWorksheetIdByName(self.BAD_SHEET_NAME)

    def test_getNumRowsInWorksheet(self):
        numRows = self.googleSheet.getNumRowsInWorksheet(self.FIRST_SHEET_NAME)
        self.assertEqual(20, numRows)
        
        #Test where worksheet is not found
        with self.assertRaises(SheetNotFoundError):
            self.googleSheet.getNumRowsInWorksheet(self.BAD_SHEET_NAME)
        
if __name__ == '__main__':
    unittest.main()