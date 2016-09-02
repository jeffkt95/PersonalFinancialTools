import win32clipboard
from Envelopes import Envelopes
from GoogleSheetInterface import GoogleSheetInterface

#TODO: consider making this a class

def main():
    fromClipboard = getClipboard()
    
    envelopes = Envelopes()
    #Take this out for now while testing the google spreadsheet stuff
    #envelopes.getEnvelopesFromQuickenExport(fromClipboard)
    print(envelopes)

    #This is the ID of my test spreadsheet right now. Note this ID is simply the URL of the spreadsheet.
    spreadsheetId = '1_tzqk8V2AsY85fZSG6svHZonFqarmaLN12g6NCznpyk'
    envelopesSpreadsheet = GoogleSheetInterface(spreadsheetId)
    envelopesSpreadsheet.connect()
    
    spreadsheetValue = envelopesSpreadsheet.getCellValue("Current period", "B3")
    print("Before change: " + str(spreadsheetValue))

    envelopesSpreadsheet.setCellValue("Current period", "B3", 1050)
    spreadsheetValue = envelopesSpreadsheet.getCellValue("Current period", "B3")
    print("After change: " + str(spreadsheetValue))
    

#TODO: Move this to its own file. I'd rather keep things modularized by file. I already
#have a file for this. I just need to make the method callable from that file.    
def getClipboard():
    #TODO: gracefully handle an empty clipboard
    win32clipboard.OpenClipboard()
    fromClipboard = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard
    return fromClipboard


if __name__ == "__main__":
    main()