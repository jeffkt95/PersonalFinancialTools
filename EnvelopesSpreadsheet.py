from GoogleSheetInterface import GoogleSheetInterface

class EnvelopesSpreadsheet(GoogleSheetInterface):
    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    SPREADSHEET_ID = '1_tzqk8V2AsY85fZSG6svHZonFqarmaLN12g6NCznpyk'
    SPENT_TOTAL_NAMED_RANGE = "SpentTotal"
    ENVELOPE_DATE_NAMED_RANGE = "AllEnvelopeData"
    AMOUNT_SPENT_NAMED_RANGE = "AmountSpent"

    def __init__(self):
        GoogleSheetInterface.__init__(self, self.SPREADSHEET_ID)
        
    def setEnvelopesInSpreadsheet(self, envelopes):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheetId, 
                                                            range=self.ENVELOPE_DATE_NAMED_RANGE).execute()
        
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
            
        totalInSpreadsheet = self.getCellValueNamedRange(self.SPENT_TOTAL_NAMED_RANGE)
        totalInQuickenExport = envelopes.getTotalExpenses()
        
        print("Total in spreadsheet after import: " + totalInSpreadsheet)
        print(          "Total in Quicken export: " + str(totalInQuickenExport))
                  
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
        
