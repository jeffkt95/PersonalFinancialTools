from Envelope import Envelope
import Utilities

class Envelopes:
    #This list has envelopes that are ignored. The only use case for the ignore list at this
    #time is parent categories where the sub-categories are specific envelopes in the list.
    #The quicken report we generate includes the parent categories and the sub-categories, so
    #if we included both we'd be double-counting.
    #Right now, the only parent/sub-categories we use are Auto (Auto:Fuel and Auto:Service)
    envelopeIgnoreList = ["Auto"]
    
    #The first line should let us know if the clipboard does indeed have the Quicken
    #report we expect. This first line is expected for these Quicken reports.
    mFirstLine = "Budget check"

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
        #First check you've got valid input
        if (qExport[:len(self.mFirstLine)] != self.mFirstLine):
            raise QuickenExportFormatError("The first line of the copy should be '" + self.mFirstLine + "'")
        
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
                elif tokens[0] == "OVERALL" and tokens[1] == "TOTAL":
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
                            
                        #First check that you're not supposed to ignore this envelope.
                        if (not envelopeName in self.envelopeIgnoreList):
                            self.addEnvelope(envelopeName, amountSpent)
    
class QuickenExportFormatError(Exception):
    def __init__(self, message):
        self.message = message
