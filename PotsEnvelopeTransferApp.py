from tkinter import *
from DoubleValueWidgets import DoubleValueWidgets
from EnvelopesSpreadsheet import EnvelopesSpreadsheet
from PotsSpreadsheet import PotsSpreadsheet
from TransferParameters import TransferParameters
from TransferProcessor import TransferProcessor

class PotsEnvelopeTransferApp:
    envelopeLastRow = 0
    potLastRow = 0
    
    potsWidgets = []
    envelopesWidgets = []
    
    def __init__(self, master):
        #Init the google spreadsheet
        self.initSpreadsheets()

        self.master = master
                
        frame = Frame(master)
        frame.pack()
        
        # Row 0 ##################################################################
        mainFrameRow = 0
        topLabel = Label(frame, text="Pots / Envelopes Transfer")
        topLabel.grid(row=mainFrameRow, column=0, columnspan=2)
        
        # Row 1 ##################################################################
        mainFrameRow += 1
        transferAmountLabel = Label(frame, text="Transfer amount:")
        transferAmountLabel.grid(row=mainFrameRow, column=0, sticky=E)
        
        transferAmount = DoubleVar()
        transferAmount.trace("w", lambda name, index, mode, 
                    transferAmount=transferAmount: self.transferAmountChanged(transferAmount))
        self.transferAmount = transferAmount
        transferAmountEntry = Entry(frame, textvariable=transferAmount)
        transferAmountEntry.grid(row=mainFrameRow, column=1, sticky=W)
        
        # Row 2 ##################################################################
        mainFrameRow += 1
        separatorLabel = Label(frame, text="_________________________________________________________________________")
        separatorLabel.grid(row=mainFrameRow, column=0, columnspan=2)

        # Row 3 ##################################################################
        mainFrameRow += 1
        fromPotFrame = Frame(frame)
        fromPotFrame.grid(row=mainFrameRow, column=0)
        
        fromSavingsPotsLabel = Label(fromPotFrame, text="From savings pots")
        fromSavingsPotsLabel.grid(row=0, column=0)
        
        addPotButton = Button(fromPotFrame, text="+", command=self.addPot)
        addPotButton.grid(row=0, column=1, sticky=E)        
        
        removePotButton = Button(fromPotFrame, text="-", command=self.removePot)
        removePotButton.grid(row=0, column=2, sticky=E)
        self.removePotButton = removePotButton
        
        transferDirectionFrame = Frame(frame)
        transferDirectionFrame.grid(row=mainFrameRow, column=1)
        
        transferDirectionButton = Button(transferDirectionFrame, text="->", command=self.changeTransferDirection)
        transferDirectionButton.grid(row=0, column=0)        
        self.transferDirectionButton = transferDirectionButton
        
        fromEnvelopeFrame = Frame(frame)
        fromEnvelopeFrame.grid(row=mainFrameRow, column=2)
        
        toCheckingEnvelopesLabel = Label(fromEnvelopeFrame, text="To checking envelopes")
        toCheckingEnvelopesLabel.grid(row=0, column=0)
        
        addEnvelopeButton = Button(fromEnvelopeFrame, text="+", command=self.addEnvelope)
        addEnvelopeButton.grid(row=0, column=1, sticky=E)        
        
        removeEnvelopeButton = Button(fromEnvelopeFrame, text="-", command=self.removeEnvelope)
        removeEnvelopeButton.grid(row=0, column=2, sticky=E)        
        self.removeEnvelopeButton = removeEnvelopeButton
        
        # Row 4 ##################################################################
        # This row has a frame for the envelopes and a frame for the pots
        mainFrameRow += 1
        self.potFrame = Frame(frame)
        self.potFrame.grid(row=mainFrameRow, column=0, sticky=N)
        
        self.envelopeFrame = Frame(frame)
        self.envelopeFrame.grid(row=mainFrameRow, column=2, sticky=N)
        
        # Add one each to start
        self.addPot()
        self.addEnvelope()
        
        # Row ##################################################################
        mainFrameRow += 1
        separatorLabel2 = Label(frame, text="_________________________________________________________________________")
        separatorLabel2.grid(row=mainFrameRow, column=0, columnspan=2)

        # Row ##################################################################
        # This row has a frame for the envelopes and a frame for the pots
        mainFrameRow += 1
        totalPotsFrame = Frame(frame)
        totalPotsFrame.grid(row=mainFrameRow, column=0, sticky=N)
        
        totalEnvelopesFrame = Frame(frame)
        totalEnvelopesFrame.grid(row=mainFrameRow, column=1, sticky=N)

        totalPotsLabel = Label(totalPotsFrame, text="Total pots:")
        totalPotsLabel.grid(row=0, column=0)
        
        self.totalPotsAmount = DoubleVar()
        totalPotsLabelAmount = Label(totalPotsFrame, text="0", textvariable=self.totalPotsAmount)
        totalPotsLabelAmount.grid(row=0, column=1)

        totalEnvelopesLabel = Label(totalEnvelopesFrame, text="Total envelopes:")
        totalEnvelopesLabel.grid(row=0, column=0)

        self.totalEnvelopesAmount = DoubleVar()
        totalEnvelopesLabelAmount = Label(totalEnvelopesFrame, text="0", textvariable=self.totalEnvelopesAmount)
        totalEnvelopesLabelAmount.grid(row=0, column=1)

        leftToTakePotsLabel = Label(totalPotsFrame, text="Left to take from pots:")
        leftToTakePotsLabel.grid(row=1, column=0)

        leftToTakeFromEnvelopesLabel = Label(totalEnvelopesFrame, text="Left to allocate to envelopes:")
        leftToTakeFromEnvelopesLabel.grid(row=1, column=0)

        self.leftToTakeFromPots = DoubleVar()
        leftToTakePotsLabelAmount = Label(totalPotsFrame, text="0", textvariable=self.leftToTakeFromPots)
        leftToTakePotsLabelAmount.grid(row=1, column=1)
        self.leftToTakePotsLabelAmount = leftToTakePotsLabelAmount

        self.leftToTakeFromEnvelopes = DoubleVar()
        leftToTakeFromEnvelopesLabelAmount = Label(totalEnvelopesFrame, text="0", textvariable=self.leftToTakeFromEnvelopes)
        leftToTakeFromEnvelopesLabelAmount.grid(row=1, column=1)
        self.leftToTakeFromEnvelopesLabelAmount = leftToTakeFromEnvelopesLabelAmount

        # Row ##################################################################
        mainFrameRow += 1
        okButton = Button(frame, text="Execute transfer", command=self.okClicked)
        okButton.grid(row=mainFrameRow, column=0)
        self.okButton = okButton
        
        cancelButton = Button(frame, text="Cancel", command=self.cancelClicked)
        cancelButton.grid(row=mainFrameRow, column=1)
        
        self.setReadyForExecuteState()
        
    def initSpreadsheets(self):
        self.envelopesSpreadsheet = EnvelopesSpreadsheet()
        self.envelopesSpreadsheet.connect()
        self.envelopeList = self.envelopesSpreadsheet.getEnvelopeList()
        
        self.potsSpreadsheet = PotsSpreadsheet()
        self.potsSpreadsheet.connect()
        self.potsList = self.potsSpreadsheet.getPotsList()
        
    def addPot(self):
        potOneVariable = StringVar(self.master)
        potOneVariable.set(self.potsList[0])
        potOneOption = OptionMenu(self.potFrame, potOneVariable, *self.potsList)
        potOneOption.grid(row=self.potLastRow, column=0)
        
        potVariable = DoubleVar()
        potVariable.trace("w", lambda name, index, mode,
                    potVariable=potVariable: self.potAmountChanged(potVariable))
        potOneAmount = Entry(self.potFrame, textvariable=potVariable)
        #Pad on the right to have space between the pots/envelopes column.
        potOneAmount.grid(row=self.potLastRow, column=1, padx=(0, 6))
        
        self.potLastRow = self.potLastRow + 1
        
        potWidgets = DoubleValueWidgets(potOneOption, potOneVariable, potOneAmount, potVariable)
        self.potsWidgets.append(potWidgets)

        self.setRemovePotButtonState()

        return potWidgets
        
    def addEnvelope(self):
        envelopeOneVariable = StringVar(self.master)
        envelopeOneVariable.set(self.envelopeList[0])
        envelopeOneOption = OptionMenu(self.envelopeFrame, envelopeOneVariable, *self.envelopeList)
        #Pad on the left to have space between the pots/envelopes column.
        envelopeOneOption.grid(row=self.envelopeLastRow, column=0, padx=(6, 0))
        
        envelopeVariable = DoubleVar()
        envelopeVariable.trace("w", lambda name, index, mode,
                    envelopeVariable=envelopeVariable: self.envelopeAmountChanged(envelopeVariable))
        envelopeOneAmount = Entry(self.envelopeFrame, textvariable=envelopeVariable)
        envelopeOneAmount.grid(row=self.envelopeLastRow, column=1)
        
        self.envelopeLastRow = self.envelopeLastRow + 1        
        
        envelopeWidgets = DoubleValueWidgets(envelopeOneOption, envelopeOneVariable, envelopeOneAmount, envelopeVariable)
        self.envelopesWidgets.append(envelopeWidgets)
        
        self.setRemoveEnvelopeButtonState()

        return envelopeWidgets

    def getEnvelopesTotal(self):
        sum = 0
        for doubleValueWidgets in self.envelopesWidgets:
            sum = sum + doubleValueWidgets.getDoubleValue()
            
        return sum
    
    def getPotsTotal(self):
        sum = 0
        for doubleValueWidgets in self.potsWidgets:
            sum = sum + doubleValueWidgets.getDoubleValue()
            
        return sum
    
    def removePot(self):
        #Get the last pot in the array. Remove its widgets from the UI, then remove the item from the list
        potWidgets = self.potsWidgets[-1]
        potWidgets.removeWidgets()
        del self.potsWidgets[-1]
        self.setRemovePotButtonState()
        self.potAmountChanged(None)

    def removeEnvelope(self):
        #Get the last envelope in the array. Remove its widgets from the UI, then remove the item from the list
        envelopesWidgets = self.envelopesWidgets[-1]
        envelopesWidgets.removeWidgets()
        del self.envelopesWidgets[-1]
        self.setRemoveEnvelopeButtonState()
        self.envelopeAmountChanged(None)

    #Fixes the state of the remove pot button. Should be disabled when there are no pots, enabled otherwise
    def setRemovePotButtonState(self):
        if (len(self.potsWidgets) == 0):
            self.removePotButton['state'] = 'disabled'
        else:
            self.removePotButton['state'] = 'normal'
            
    #Fixes the state of the remove pot button. Should be disabled when there are no pots, enabled otherwise
    def setRemoveEnvelopeButtonState(self):
        if (len(self.envelopesWidgets) == 0):
            self.removeEnvelopeButton['state'] = 'disabled'
        else:
            self.removeEnvelopeButton['state'] = 'normal'
            
    def okClicked(self):
        transferParameters = TransferParameters(self.transferAmount.get(), True)
        
        for pot in self.potsWidgets:
            transferParameters.addPot(pot.getSelectedName(), pot.getDoubleValue())
            
        for envelope in self.envelopesWidgets:
            transferParameters.addEnvelope(envelope.getSelectedName(), envelope.getDoubleValue())
            
        print("Finished getting transferParameters from UI")
        print(transferParameters)
        
        transferProcessor = TransferProcessor(transferParameters, self.potsSpreadsheet, self.envelopesSpreadsheet)
        transferProcessor.processTransfer()

    def cancelClicked(self):
        print("TODO: implement cancelClicked")
        
    #This method sets color and state for different widgets based on whether or not the 
    #transfer is ready for execution.
    def setReadyForExecuteState(self):
        #If there's a non-zero transfer amount, and the pots and envelopes add up to that amount
        #(i.e. there's nothing left to take from/allocate to them), then it's ready for execution
        
        print("In setReadyForExecuteState")
        if (self.transferAmount.get() > 0.0 and 
                self.leftToTakeFromPots.get() == 0 and 
                self.leftToTakeFromEnvelopes.get() == 0):
            self.okButton['state'] = 'normal'
            self.leftToTakePotsLabelAmount['foreground'] = 'green'
            self.leftToTakeFromEnvelopesLabelAmount['foreground'] = 'green'
        else:
            self.okButton['state'] = 'disabled'
            if (self.leftToTakeFromPots.get() == 0.0 and self.transferAmount.get() > 0.0):
                self.leftToTakePotsLabelAmount['foreground'] = 'green'
            else:
                self.leftToTakePotsLabelAmount['foreground'] = 'red'
                
            if (self.leftToTakeFromEnvelopes.get() == 0.0 and self.transferAmount.get() > 0.0):
                self.leftToTakeFromEnvelopesLabelAmount['foreground'] = 'green'
            else:
                self.leftToTakeFromEnvelopesLabelAmount['foreground'] = 'red'
    
    def envelopeAmountChanged(self, envelopeAmountVariable):
        try:
            transferAmount = self.transferAmount.get()
            totalEnvelopes = self.getEnvelopesTotal()
            self.totalEnvelopesAmount.set(totalEnvelopes)
            self.leftToTakeFromEnvelopes.set(transferAmount - totalEnvelopes)
            self.setReadyForExecuteState()
        except:
            print("Exception, envelopeAmountChanged")
            pass
            
    def potAmountChanged(self, potAmountVariable):
        try:
            print("Debug 1")
            transferAmount = self.transferAmount.get()
            print("Debug 2")
            totalPots = self.getPotsTotal()
            print("Debug 3")
            self.totalPotsAmount.set(totalPots)
            print("Debug 4")
            self.leftToTakeFromPots.set(transferAmount - totalPots)
            print("Debug 5")
            self.setReadyForExecuteState()
            print("Debug 6")
        except:
            print("Exception, potAmountChanged")
            pass
    
    def transferAmountChanged(self, transferAmountVariable):
        try:
            self.envelopeAmountChanged(None)
            self.potAmountChanged(None)
            self.setReadyForExecuteState()
        except:
            print("Exception, transferAmountChanged")
            pass
        
    def changeTransferDirection(self):
        print("Hello")
    
def main():
    root = Tk()
    app = PotsEnvelopeTransferApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    