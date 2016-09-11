from tkinter import *

class PotsEnvelopeTransferApp:
    envelopeLastRow = 0
    potLastRow = 0
    
    def __init__(self, master):
        self.master = master
        
        frame = Frame(master)
        frame.pack()
        
        # Row 0 ##################################################################
        topLabel = Label(frame, text="Pots -> Envelopes Transfer")
        topLabel.grid(row=0, column=0, columnspan=4)
        
        # Row 1 ##################################################################
        transferAmountLabel = Label(frame, text="Transfer amount:")
        transferAmountLabel.grid(row=1, column=0, columnspan=2, sticky=E)
        
        transferAmountEntry = Entry(frame)
        transferAmountEntry.grid(row=1, column=2, columnspan=2, sticky=W)
        
        # Row 2 ##################################################################
        separatorLabel = Label(frame, text="___________________________________________________________________")
        separatorLabel.grid(row=2, column=0, columnspan=4)

        # Row 3 ##################################################################
        fromSavingsPotsLabel = Label(frame, text="From savings pots")
        fromSavingsPotsLabel.grid(row=3, column=0, columnspan=2)
        
        toCheckingEnvelopesLabel = Label(frame, text="To checking envelopes")
        toCheckingEnvelopesLabel.grid(row=3, column=2, columnspan=2)
        
        # Row 4 ##################################################################
        # This row has a frame for the envelopes and a frame for the pots
        self.potFrame = Frame(frame)
        self.potFrame.grid(row=4, column=0, columnspan=2, sticky=N)
        
        self.envelopeFrame = Frame(frame)
        self.envelopeFrame.grid(row=4, column=2, columnspan=2, sticky=N)
        
        # Add one each to start
        self.addPot()
        self.addEnvelope()
        
        # Row 5 ##################################################################
        addPotButton = Button(frame, text="+", command=self.addPot)
        addPotButton.grid(row=5, column=0, sticky=W)        
        
        addEnvelopeButton = Button(frame, text="+", command=self.addEnvelope)
        addEnvelopeButton.grid(row=5, column=2, sticky=W)        
        
        # Row 6 ##################################################################
        okButton = Button(frame, text="OK", command=self.okClicked)
        okButton.grid(row=6, column=0, columnspan=2)
        
        cancelButton = Button(frame, text="Cancel", command=self.cancelClicked)
        cancelButton.grid(row=6, column=2, columnspan=2)
        
    def addPot(self):
        potOneVariable = StringVar(self.master)
        potOneVariable.set("Car")
        potOneOption = OptionMenu(self.potFrame, potOneVariable, "Car", "Charity", "Rainy day")
        potOneOption.grid(row=self.potLastRow, column=0)
        
        potOneAmount = Entry(self.potFrame)
        potOneAmount.grid(row=self.potLastRow, column=1)

        self.potLastRow = self.potLastRow + 1
        
    def addEnvelope(self):
        envelopeOneVariable = StringVar(self.master)
        envelopeOneVariable.set("Car")
        envelopeOneOption = OptionMenu(self.envelopeFrame, envelopeOneVariable, "Car", "Charity", "Rainy day")
        envelopeOneOption.grid(row=self.envelopeLastRow, column=0)
        
        envelopeOneAmount = Entry(self.envelopeFrame)
        envelopeOneAmount.grid(row=self.envelopeLastRow, column=1)
        
        self.envelopeLastRow = self.envelopeLastRow + 1        

    def okClicked(self):
        print("TODO: implement okClicked")

    def cancelClicked(self):
        print("TODO: implement cancelClicked")

def main():
    root = Tk()
    app = PotsEnvelopeTransferApp(root)

    print("Entering mainloop")
    root.mainloop()
    print("Done in mainloop")

if __name__ == "__main__":
    main()
    