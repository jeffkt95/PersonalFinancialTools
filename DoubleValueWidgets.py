#This class represents a double and some associated widgets 

class DoubleValueWidgets:
    def __init__(self, option, entry, doubleVariable):
        self.option = option
        self.entry = entry
        self.doubleVariable = doubleVariable
        
    def getDouble(self):
        return self.doubleVariable.get()
        
        