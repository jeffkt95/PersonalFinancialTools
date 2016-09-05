from Envelopes import Envelopes
from GoogleSheetInterface import GoogleSheetInterface
from EnvelopesSpreadsheet import EnvelopesSpreadsheet
import Utilities

def main():
    fromClipboard = Utilities.getClipboard()
    
    envelopes = Envelopes()
    envelopes.getEnvelopesFromQuickenExport(fromClipboard)
    
    envelopesSpreadsheet = EnvelopesSpreadsheet()
    envelopesSpreadsheet.connect()
    envelopesSpreadsheet.setEnvelopesInSpreadsheet(envelopes)
    
    wait = input("PRESS ENTER TO CONTINUE.")
    
if __name__ == "__main__":
    main()