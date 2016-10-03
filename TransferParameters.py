from Envelope import Envelope

class TransferParameters:
    envelopes = []
    pots = []
    
    ENVELOPES = "Envelopes"
    POTS = "Pots"
    transferTo = ENVELOPES
    
    def __init__(self, transferAmount, transferTo):
        #Clear the arrays
        self.envelopes = []
        self.pots = []
        
        self.transferAmount = transferAmount
        self.transferTo = transferTo
        
    def addEnvelope(self, name, value):
        self.envelopes.append(Envelope(name, value))
        
    def addPot(self, name, value):
        self.pots.append(Envelope(name, value))
        
    def getTransferTo(self):
        return self.transferTo
        
    def getTransferAmount(self):
        return self.transferAmount
    
    def __str__(self):
        string = "Transfer, amount: " + str(self.transferAmount) + "\n"
        
        if (self.transferTo == self.ENVELOPES):
            string = string + "  Transfer goes from pots to envelopes\n"
        else:
            string = string + "  Transfer goes from envelopes to pots\n"
            
        string = string + "  Pots:\n"
        for pot in self.pots:
            string = string + "    " + str(pot) + "\n"
        
        string = string + "  Envelopes:\n"
        for envelope in self.envelopes:
            string = string + "    " + str(envelope) + "\n"
        
        return string
