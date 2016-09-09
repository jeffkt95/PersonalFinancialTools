# PersonalFinancialTools
A set of tools for my personal finances.

## ENVELOPE SCRIPT
This is mostly done now.

## POTS AUTOMATION
### Use cases
#### Use case 1, pots to envelopes-
* User enters total transfer amount
* Interface has two columns:
From savings pots    |   To checking envelopes

* The columns either list all the pots/envelopes, or it has pulldowns that allow you to add new pots/envelopes
* Each row within the column as the pulldown and a text field. The text field is where you enter the amount.
* at the bottom (or top?) you have a running total of the pots/envelopes you've entered so far.
* 

#### Use case 2, envelopes to pots-

#### Use case 3, checking/paycheck to pots-

#### Use case 4, pots to checking balance, manual envelope adjustment-
This one might be the most practical. It's also probably one of the easiest to implement. You might want to start with it.
* Manually enter the amount you're taking out of savings
* The tool enters the new savings balance
* OR
* Enter the new savings balance
* 

### UI Mockup. 'v' means pulldown.

```
         Pots -> Envelopes Transfer
Transfer amount  _____________
---------------------------------------
From savings pots        |   To checking envelopes
v Car __200__            |   v Auto:Service __200__
v Rainy day __550__      |   v Clothing __20___
                         |   v Dining   __100__
-------------------------------------------                         
Total pots: 750          |   Total envelopes: 320
Left to take from pots:  |   Left to allocate to envelopes: 
-------------------------------------------
     OK                           Cancel
(The OK button will be disabled until the pots and envelopes totals match the transfer amount.)
```

# TODO
* Start working on the GUI. Prototype it out. Particularly...
  * Adding new spots for pots/envelopes. By default there will only be one
  * Modifying totals based on user input
  * Enable/disable OK button based on totals matching. 
  * Fill pulldown options with envelopes/pots
* Implement classes required for back-end code.
  * Envelopes. Parse the envelopes spreadsheet and store them. (I alreaady have code to do this.)
  * Pots. Parse the pots spreadsheet and store them. Will be very similar to the envelopes code I already implemented this.
* Execute the transfer.
  * In pots spreadsheet:
    * Add a column, copy previous
    * Decrement the savings balance by the transfer amount
    * Adjust the pots based on the inputs
  * In the envelopes spreadsheet
    * Increase the total at the top
    * Adjust the envelopes based on the inputs
