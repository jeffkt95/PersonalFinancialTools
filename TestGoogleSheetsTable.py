import unittest
from GoogleSheetsTable import GoogleSheetsTable
from GoogleSheetInterface import GoogleSheetInterface

class TestGoogleSheetInterface(unittest.TestCase):
    UNIT_TEST_SPREADSHEET_ID = "1DVuL4Pf5KfblavC8X92p62oCU_cTxgfUBWloQcwsmsE"
    SHEET_NAME = "Table tests"

    def setUp(self):
        self.googleSheet = GoogleSheetInterface(self.UNIT_TEST_SPREADSHEET_ID)
        self.googleSheet.connect()
        
        self.mNameAgeTable = GoogleSheetsTable(self.googleSheet, "A", "B", 3, 6, self.SHEET_NAME)
        self.mNameSalaryTable = GoogleSheetsTable(self.googleSheet, "A", "C", 3, 6, self.SHEET_NAME)
        self.mArtistTable = GoogleSheetsTable(self.googleSheet, "E", "F", 6, 11, self.SHEET_NAME)
    
    #def tearDown(self):
        #Nothing to do
        
    def test_getKeysList(self):
        nameKeysList = self.mNameAgeTable.getKeysList()
        artistKeysList = self.mArtistTable.getKeysList()
        
        self.assertEqual(nameKeysList[0], "Roy");
        self.assertEqual(nameKeysList[1], "Joe");
        self.assertEqual(nameKeysList[2], "Fred");
        self.assertEqual(nameKeysList[3], "Phyllis");
    
        self.assertEqual(artistKeysList[0], "Sting");
        self.assertEqual(artistKeysList[1], "Cher");
        self.assertEqual(artistKeysList[2], "David Bowie");
        self.assertEqual(artistKeysList[3], "Aerosmith");
        self.assertEqual(artistKeysList[4], "Rolling Stones");
        self.assertEqual(artistKeysList[5], "Adam Levine");

    def test_addToTableRow(self):
        self.assertEqual(1, 2)
    
        
if __name__ == '__main__':
    unittest.main()