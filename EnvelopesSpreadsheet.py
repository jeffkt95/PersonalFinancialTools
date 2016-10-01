from GoogleSheetInterface import GoogleSheetInterface
from GoogleSheetsTable import GoogleSheetsTable
import Utilities

class EnvelopesSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    TEST_SPREADSHEET_ID = '1_tzqk8V2AsY85fZSG6svHZonFqarmaLN12g6NCznpyk'
    REAL_SPREADSHEET_ID = '1ZCOhZ7KIo9ZsIsoNhvvvWOqsdLFo8rCesosLZ6tOlh0'
    SPENT_TOTAL_NAMED_RANGE = "SpentTotal"
    ENVELOPE_DATE_NAMED_RANGE = "AllEnvelopeData"
    AMOUNT_SPENT_NAMED_RANGE = "AmountSpent"

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.TEST_SPREADSHEET_ID)
        self.mEnvelopesTable = GoogleSheetsTable(self, "A", "B", 3, 32, "Current period")
        
    def getEnvelopesTable(self):
        return self.mEnvelopesTable
        
    def loadEnvelopeData(self):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                            range=self.ENVELOPE_DATE_NAMED_RANGE).execute()
        return result
        
    def setEnvelopesInSpreadsheet(self, envelopes):
        result = self.loadEnvelopeData()
        
        envelopeData = result.get('values', [])
        
        if not envelopeData:
            print("There was a problem getting envelope data from the spreadsheet. It returned null.")
            return
            
        #Create empty array to store the amount spent data in the right slot
        amountSpent = [[""] for x in range(len(envelopeData))]

        for envelope in envelopes:
            amountSpent = self.setEnvelopeInSpreadsheet(envelope, envelopeData, amountSpent)
            
        #Shoving the modified data back in.
        myBody = {u'range': self.AMOUNT_SPENT_NAMED_RANGE, u'values': amountSpent, u'majorDimension': u'ROWS'}
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheetId, range=self.AMOUNT_SPENT_NAMED_RANGE, body=myBody, valueInputOption='USER_ENTERED').execute()
            
        totalInSpreadsheet = Utilities.getNumber(self.getCellValueNamedRange(self.SPENT_TOTAL_NAMED_RANGE))
        totalInQuickenExport = envelopes.getTotalExpenses()
        
        if (totalInSpreadsheet == totalInQuickenExport):
            print("")
            print("---------------------  SUCCESS  ---------------------")
            print("     Successfully copied Quicken data into envelopes.")
            print("     Total spent from envelopes: $" + str(totalInSpreadsheet))
            print("")
        else:
            print("")
            print("********************  WARNING!  ********************")
            print("     Quicken data was copied into envelopes, but the totals don't match.")
            print("         Quicken total: $" + str(totalInQuickenExport))
            print("       Envelopes total: $" + str(totalInSpreadsheet))
            print("       A difference of: $" + str(totalInQuickenExport - totalInSpreadsheet))
            print("")
            print("     Try visually comparing the Quicken report to the envelope spreadsheet.")
            print("     And report the problem to Jeff.")
            print("")
        
    #This method takes in the envelopeData, finds the particular envelope, then sets the data
    def setEnvelopeInSpreadsheet(self, envelope, envelopeData, amountSpent):
        envelopeName = envelope.getName()
        envelopeSpent = envelope.getAmountSpent()

        for i in range(0, len(envelopeData)):
            if (envelopeData[i][0] == envelopeName):
                amountSpent[i] = [envelopeSpent]
                #print("Envelope " + envelopeName + " amount spent changed to " + str(envelopeSpent))
                return amountSpent
                
        #If you get down here without returning, you never found the envelope. Return envelopeData unmodified
        print("Never found envelope " + envelopeName + "! " + str(envelopeSpent) + " won't be included.")
        return amountSpent
        
