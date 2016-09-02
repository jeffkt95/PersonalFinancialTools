from Envelope import Envelope
import datetime

class Envelopes:

    def __init__(self):
        self.envelopes = []
        self.totalExpenses = 0
        
    def addEnvelope(self, name, amountSpent):
        newEnvelope = Envelope(name, amountSpent)
        self.envelopes.append(newEnvelope)
        
    def __str__(self):
        string = "Envelopes:\n"
        for envelope in self.envelopes:
            string = string + "    " + str(envelope) + "\n"
        
        string = string + "TOTAL EXPENSES: " + self.totalExpenses
        return string
        
    def getEnvelopesFromQuickenExport(self, qExport):
        envelopeListStarted = False
        
        lines = qExport.split("\n")
        
        for line in lines:
            print("Reading " + line)
            tokens = line.split()
            if (len(tokens) < 2):
                continue
                
            if (not envelopeListStarted and tokens[0] == "EXPENSES"):
                self.totalExpenses = tokens[1]
                envelopeListStarted = True
            elif (envelopeListStarted):
                if self.isDate(tokens[0]):
                    #skip it. That's an envelopes detailed breakdown. Not interested in that
                    continue
                elif tokens[0] == "OVERALL TOTAL":
                    #You're done. Break out
                    break;
                else:
                    #Found an envelope!
                    self.addEnvelope(tokens[0], tokens[1])
    
    def isDate(self, possibleDate):
        try:
            datetime.datetime.strptime(possibleDate, '%m/%d/%Y')
            return True
        except ValueError:
            return False
