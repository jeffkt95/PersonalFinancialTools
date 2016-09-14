from Envelope import Envelope

class TransferParameters:
    envelopes = []
    pots = []
    
    #potsToEnvelopes is a bool. If true, the transfer goes from pots to envelopes
    #       If false, transfer is from envelopes to pots
    def __init__(self, transferAmount, potsToEnvelopes):
        self.transferAmount = transferAmount
        self.potsToEnvelopes = potsToEnvelopes
        
    def addEnvelope(self, name, value):
        self.envelopes.append(Envelope(name, value))
        
    def addPot(self, name, value):
        self.pots.append(Envelope(name, value))
        
    def getPotsToEnvelopesBool():
        return self.potsToEnvelopes
    
    def __str__(self):
        string = "Transfer, amount: " + str(self.transferAmount) + "\n"
        
        if (self.potsToEnvelopes):
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
