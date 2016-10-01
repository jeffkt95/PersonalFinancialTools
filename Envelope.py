#This class says is called envelope, but it could also represent a pot.
class Envelope:
    
    def __init__(self, name, amountSpent):
        self.name = name
        self.amountSpent = amountSpent
        
    def getName(self):
        return self.name
        
    def getAmountSpent(self):
        return self.amountSpent
        
    def __str__(self):
        string = "Envelope " + self.name + ", amount spent: " + str(self.amountSpent)
        return string