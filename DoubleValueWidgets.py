#This class represents a double and some associated widgets 

class DoubleValueWidgets:
    def __init__(self, option, nameVariable, entry, doubleVariable):
        self.option = option
        self.nameVariable = nameVariable
        self.entry = entry
        self.doubleVariable = doubleVariable
        
    def getDoubleValue(self):
        return self.doubleVariable.get()
        
    def getSelectedName(self):
        return self.nameVariable.get()
        
    def removeWidgets(self):
        self.option.grid_remove()
        self.entry.grid_remove()
        #Should I remove the doubleVariable? If so, how do I do it?