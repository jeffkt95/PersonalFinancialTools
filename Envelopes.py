from Envelope import Envelope
import Utilities

class Envelopes:

    def __init__(self):
        self.envelopes = []
        self.totalExpenses = 0
        
        #Used for itertion
        self.envelopeIndex = 0
        
    def addEnvelope(self, name, amountSpent):
        newEnvelope = Envelope(name, amountSpent)
        self.envelopes.append(newEnvelope)
        
    def getTotalExpenses(self):
        return self.totalExpenses
        
    def __str__(self):
        string = "Envelopes:\n"
        for envelope in self.envelopes:
            string = string + "    " + str(envelope) + "\n"
        
        string = string + "TOTAL EXPENSES: " + str(self.totalExpenses)
        return string
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if (self.envelopeIndex >= len(self.envelopes)):
            raise StopIteration
        else:
            self.envelopeIndex += 1
            return self.envelopes[self.envelopeIndex - 1]
        
    def getEnvelopesFromQuickenExport(self, qExport):
        envelopeListStarted = False
        
        lines = qExport.split("\n")
        
        for line in lines:
            tokens = line.split()
            if (len(tokens) < 2):
                continue
                
            if (not envelopeListStarted and tokens[0] == "EXPENSES"):
                self.totalExpenses = Utilities.reverseSign(tokens[1])
                envelopeListStarted = True
            elif (envelopeListStarted):
                if Utilities.isDate(tokens[0]):
                    #skip it. This line is an individual transaction. Not interested in that
                    continue
                elif tokens[0] == "OVERALL TOTAL":
                    #You're done. Break out
                    break;
                else:
                    #Found an envelope!
                    #The last token is the amount spent. (Check that it's numeric.)
                    #The tokens before it make up the envelope name. (They could have spaces.)
                    amountSpent = tokens[len(tokens) - 1]
                    #Only proceed if the amount spent is a number
                    if (Utilities.is_number(amountSpent)):
                        #Amount spent comes in from Quicken as a negative. You want it positive (amount SPENT). So
                        #   reverse the sign.
                        amountSpent = Utilities.reverseSign(amountSpent)
                        
                        #Next piece the envelope name back together. Go until the second to last one (excluding the amount spent)
                        envelopeName = ""
                        for i in range(0, len(tokens) - 1):
                            if (i==0):
                                envelopeName = tokens[i]
                            else:
                                envelopeName = envelopeName + " " + tokens[i]
                            
                        self.addEnvelope(envelopeName, amountSpent)
    
