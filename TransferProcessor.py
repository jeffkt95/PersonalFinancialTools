#This class takes in all the data required to do the transfer. The class also has the logic
# to actually perform the transfer.
class TransferProcessor:
    
    def __init__(self, transferParameters, potsSpreadsheet, envelopesSpreadsheet):
        self.transferParameters = transferParameters
        self.potsSpreadsheet = potsSpreadsheet
        self.envelopesSpreadsheet = envelopesSpreadsheet
        
    def processTransfer(self):
        # TODO: change processing based on this bool:
        #if (self.transferParameters.getPotsToEnvelopesBool()):
         
        #iterate 
        
        result = self.envelopesSpreadsheet.loadEnvelopeData()
        
        envelopeData = result.get('values', [])
        
        theRange = result.get('range')
        
        print("The range for what I just got is: " + theRange)
