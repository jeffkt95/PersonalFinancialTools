from TransferParameters import TransferParameters

#This class takes in all the data required to do the transfer. The class also has the logic
# to actually perform the transfer.
class TransferProcessor:
    def __init__(self, transferParameters, potsSpreadsheet, envelopesSpreadsheet):
        self.transferParameters = transferParameters
        self.mPotsSpreadsheet = potsSpreadsheet
        self.mEnvelopesSpreadsheet = envelopesSpreadsheet
        self.mPotsTable = potsSpreadsheet.getPotsTable()
        self.mEnvelopesTable = envelopesSpreadsheet.getEnvelopesTable()
        
    def processTransfer(self):
        self.processPots()
        self.processEnvelopes()
        
    def processPots(self):
        #If there are no pots, nothing to do.
        if (len(self.transferParameters.pots) == 0):
            return

        #If going from pots to envelopes, then pots values should be multiplied by -1, so you're subtracting the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.POTS):
            factor = 1
        else:
            factor = -1
            
        self.mPotsSpreadsheet.copyPasteShiftPreviousPots()
        
        self.mPotsSpreadsheet.addToTotal(self.transferParameters.getTransferAmount() * factor)
        
        self.mPotsSpreadsheet.setPotsNote(self.transferParameters.getPotsNote())
        
        for pot in self.transferParameters.pots:
            self.mPotsTable.addToTableRow(pot.getName(), pot.getAmountSpent() * factor)
    
    def processEnvelopes(self):
        #If there are no envelopes, nothing to do.
        if (len(self.transferParameters.envelopes) == 0):
            return
            
        #If going from pots to envelopes, then envelope values should be multiplied by 1, so you're adding the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.ENVELOPES):
            factor = 1
        else:
            factor = -1
            
        self.mEnvelopesSpreadsheet.addToTotal(self.transferParameters.getTransferAmount() * factor)

        for envelope in self.transferParameters.envelopes:
            self.mEnvelopesTable.addToTableRow(envelope.getName(), envelope.getAmountSpent() * factor)
                        