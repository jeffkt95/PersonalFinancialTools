from TransferParameters import TransferParameters
from EmailMessage import EmailMessage
from Passwords import Passwords
from tkinter import *
import tkinter
import tkinter.simpledialog
import Utilities

smtpServer = "smtp.gmail.com"
smtpUsername = "jeffkt95@gmail.com"
fromAddress = "jeffkt95@gmail.com"
toAddress = "jeffkt@alum.mit.edu"

#This class takes in all the data required to do the transfer. The class also has the logic
# to actually perform the transfer.
class TransferProcessor:
    def __init__(self, transferParameters, potsSpreadsheet, envelopesSpreadsheet):
        self.transferParameters = transferParameters
        self.mPotsSpreadsheet = potsSpreadsheet
        self.mEnvelopesSpreadsheet = envelopesSpreadsheet
        self.mPotsTable = potsSpreadsheet.getPotsTable()
        self.mEnvelopesTable = envelopesSpreadsheet.getEnvelopesTable()
        
    def processTransfer(self):
        self.processPots()
        self.processEnvelopes()
        self.documentWithEmail()
        
    def processPots(self):
        #If there are no pots, nothing to do.
        if (len(self.transferParameters.pots) == 0):
            return

        #If going from pots to envelopes, then pots values should be multiplied by -1, so you're subtracting the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.POTS):
            factor = 1
        else:
            factor = -1
            
        self.mPotsSpreadsheet.copyPasteShiftPreviousPots()
        
        self.mPotsSpreadsheet.addToTotal(self.transferParameters.getTransferAmount() * factor)
        
        self.mPotsSpreadsheet.setPotsNote(self.transferParameters.getPotsNote())
        
        for pot in self.transferParameters.pots:
            self.mPotsTable.addToTableRow(pot.getName(), pot.getAmountSpent() * factor)
    
    def processEnvelopes(self):
        #If there are no envelopes, nothing to do.
        if (len(self.transferParameters.envelopes) == 0):
            return
            
        #If going from pots to envelopes, then envelope values should be multiplied by 1, so you're adding the amount
        if (self.transferParameters.getTransferTo() == TransferParameters.ENVELOPES):
            factor = 1
        else:
            factor = -1
            
        self.mEnvelopesSpreadsheet.addToTotal(self.transferParameters.getTransferAmount() * factor)

        for envelope in self.transferParameters.envelopes:
            self.mEnvelopesTable.addToTableRow(envelope.getName(), envelope.getAmountSpent() * factor)
                        
    def documentWithEmail(self):        
        messageBody = "Total transfer amount: " + Utilities.formatAsDollars(self.transferParameters.getTransferAmount())
        
        #If there are no pots, nothing to do.
        if (len(self.transferParameters.pots) == 0):
            messageBody = messageBody + "\n\nThis transfer does affect pots."
        if (len(self.transferParameters.envelopes) == 0):
            messageBody = messageBody + "\n\nThis transfer does affect envelopes."

        if (self.transferParameters.getTransferTo() == TransferParameters.POTS):
            subject = "Envelopes -> Pots transfer executed"
            potsHeader = "Money transferred into pots:"
            envelopesHeader = "Money transferred from envelopes:"
        else:
            subject = "Pots -> Envelopes transfer executed"
            potsHeader = "Money transferred from pots:"
            envelopesHeader = "Money transferred into envelopes:"

        messageBody = messageBody + "\n\n" + potsHeader
        for pot in self.transferParameters.pots:
            messageBody = messageBody + "\n" + Utilities.formatAsDollars(pot.getAmountSpent()) + "     " + pot.getName()


        messageBody = messageBody + "\n\n" + envelopesHeader
        for envelope in self.transferParameters.envelopes:
            messageBody = messageBody + "\n" + Utilities.formatAsDollars(envelope.getAmountSpent()) + "     " + envelope.getName()

        messageBody = messageBody + "\n\nTransfer note:"
        messageBody = messageBody + "\n" + self.transferParameters.getPotsNote()
        
        messageBody = messageBody + "\n\nHave a nice day!"
        
        #password = tkinter.simpledialog.askstring("Password", "Enter email server password\nfor user " + smtpUsername + ": ", show='*')
        passwords = Passwords()
        password = passwords.retrievePassword(smtpUsername)
        emailMessage = EmailMessage(smtpServer, fromAddress, subject, smtpUsername, password)
        emailMessage.addPlainTextBody(messageBody)
        emailMessage.send(toAddress, toAddress)
