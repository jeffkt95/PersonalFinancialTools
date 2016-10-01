from TransferParameters import TransferParameters

#This class takes in all the data required to do the transfer. The class also has the logic
# to actually perform the transfer.
class TransferProcessor:
    def __init__(self, transferParameters, potsTable, envelopesTable):
        self.transferParameters = transferParameters
        self.mPotsTable = potsTable
        self.mEnvelopesTable = envelopesTable
        
    def processTransfer(self):
        self.processPots()
        self.processEnvelopes()
        
    def processPots(self):
        #If going from pots to envelopes, then pots values should be multiplied by -1, so you're subtracting the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.POTS):
            factor = 1
        else:
            factor = -1
            
        for pot in self.transferParameters.pots:
            print("Adding to pot " + pot.getName())
            self.mPotsTable.addToTableRow(pot.getName(), pot.getAmountSpent() * factor)
    
    def processEnvelopes(self):
        #If going from pots to envelopes, then envelope values should be multiplied by 1, so you're adding the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.ENVELOPES):
            factor = 1
        else:
            factor = -1
            
        for envelope in self.transferParameters.envelopes:
            print("Adding to envelope " + envelope.getName())
            self.mEnvelopesTable.addToTableRow(envelope.getName(), envelope.getAmountSpent() * factor)
                        