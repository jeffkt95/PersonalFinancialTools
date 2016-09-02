import win32clipboard
from Envelopes import Envelopes

#TODO: consider making this a class

def main():
    fromClipboard = getClipboard()
    
    envelopes = Envelopes()
    
    envelopes.getEnvelopesFromQuickenExport(fromClipboard)
    #envelopes.addEnvelope("Dining", 20.00)
    #envelopes.addEnvelope("Gas", 124.23)
    
    print(envelopes)
    
    
def getClipboard():
    #TODO: gracefully handle an empty clipboard
    win32clipboard.OpenClipboard()
    fromClipboard = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard
    return fromClipboard


if __name__ == "__main__":
    main()