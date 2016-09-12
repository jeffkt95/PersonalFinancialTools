#This class represents a double and some associated widgets 

class DoubleValueWidgets:
    def __init__(self, option, entry, doubleVariable):
        self.option = option
        self.entry = entry
        self.doubleVariable = doubleVariable
        
    def getDouble(self):
        return self.doubleVariable.get()
        
    def removeWidgets(self):
        self.option.grid_remove()
        self.entry.grid_remove()
        #Should I remove the doubleVariable? If so, how do I do it?