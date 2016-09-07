from Envelopes import Envelopes
from GoogleSheetInterface import GoogleSheetInterface
from EnvelopesSpreadsheet import EnvelopesSpreadsheet
from Envelopes import QuickenExportFormatError
import Utilities
import sys
import traceback

def main():
    try:
        fromClipboard = Utilities.getClipboard()
        
        envelopes = Envelopes()
        envelopes.getEnvelopesFromQuickenExport(fromClipboard)
        
        envelopesSpreadsheet = EnvelopesSpreadsheet()
        envelopesSpreadsheet.connect()
        envelopesSpreadsheet.setEnvelopesInSpreadsheet(envelopes)
    except QuickenExportFormatError as err:
        print("")
        print("xxxxxxxxxxxxxxxxxxxxxxx  Error!  xxxxxxxxxxxxxxxxxxxxxxx")
        print("   Did you forget to copy from the Quicken report first?")
        print("")
        print("   Try again, but make sure you first copy the Quicken report")
        print("   by selecting 'Export', then 'Copy report to clipboard'")
        print("")
        print("   Error message: " + err.message)
        print("")
    except:
        print("")
        print("xxxxxxxxxxxxxxxxxxxxxxx  Failure!  xxxxxxxxxxxxxxxxxxxxxxx")
        print("   Unexpected error....")
        traceback.print_tb(sys.exc_info()[2])
        print("")
        print("Contact Mr. Jeffrey for technical support.")
        print("")
        raise
    
    wait = input("Press enter to close this window.")
    
if __name__ == "__main__":
    main()
    