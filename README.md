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
### Design: Tables and Named Ranges
I need to be able to find names in a table, then to that row, set the value in an another column.
The google api doesn't give a straightforward way of doing that. There's no "match" function that
is part of the API. What I did in the envelopes implementation is set all the values, leaving empty
the ones I didn't have. This is what is wanted in envelopes, but pots is different. I only want
to change the ones I have values for.

So I need to do a "get" for the whole table, then when I find the row, offset over and set the value for that
same row. There's a couple ways I can think of doing this.

1. Just do the request based on a hard-coded range in the code, not with a named range. There's difficulties with 
using a named range, and I ultimately need spreadsheet knowledge in the code. So I might as well just hard-code that in,
and use that knowledge to offset to the column I'm setting
2. Use a named range for the row keys (e.g. envelope names), and a separate named range for the row values. This way I know
the column. I'll have to get the range address to figure out which row the data is actually in. Then I'll set the data, not 
using the named range, but using the column letter I get from the named range, and the row number I can determine from the 
keys address row and the number in the array.
So for example:
    a. get potNames table
    b. Get the potNames address. Extract the starting row.
    c. find Car pot in table. Save the row I found it in
    d. rowForValue = starting row + row found
    e. Get pot values address. Extract the column.
    f. Set the pot value in cell (column from step E)(row from step D)
So complicated and hacky!
3. In the spreadsheet classes, just have the following variables:

tableKeyColumn = <column letter>
tableValueColumn = <column letter>
tableStartRow = <row number>
tableEndRow = <row number>
tableSheetName = <string>

That fully defines the spreadsheet table! Whether or not you hard-code those values, or get them from the spreadsheet with named ranges,
I think having variables for these is necessary. So assuming you have those values ready:
    a. get data from 'tableSheetName'! + tableKeyColumn + tableStartRow + ":" + tableKeyColumn + tableEndRow
    b. Find Car pot in data returned from step a. Save the row it was found in.
    c. rowForValue = tableStartRow + row found
    d. set the pot value in cell 'tableSheetName'! + tableValueColumn + ":" + rowForValue

I like the idea of determining the table variables (tableKeyColumn, tableStartRow, etc.) one time based on named ranges, then not
using the named ranges again. Assuming I don't just use the hard codes. Start with the hard codes, then decide if you want
to determine the table variables from named ranges.

# TODO
* Implement the GUI
  * DONE Adding new spots for pots/envelopes. By default there will only be one
  * DONE Modifying totals based on user input
  * DONE Add ability to remove spots for pots/envelopes. Just remove the bottom one. You have to remove it from the UI and the array/list.
  * DONE Enable/disable OK button based on totals matching. 
  * DONE Do some green/red color coding based on whent the totals match and are ready to go.
  * DONE Fill pulldown options with envelopes/pots
    * Done, except hidden rows are killing me. No API for this. Try adapting this workaround to the python API: https://code.google.com/p/google-apps-script-issues/issues/detail?id=195#c50
    * Since API doesn't support querying if row is hidden, and the workaround is a messy hack not even implemented in the python API, I'll instead move the hidden rows below the unhidden ones, and only include the unhidden, active rows in the named range.
      * Do this for both the test spreadsheet and the real one.
  * I had to change some of the classes that the other app uses, "Copy Quicken into spreadsheet" app. I need to test that I didn't break anything.
  * Add buttons to launch the pots and envelope spreadsheets
  * DONE Add space/buffer between the pots and envelope columns
* Implement classes required for back-end code.
  * Envelopes. An array of objects with the values put in the GUI
  * Pots. An array of objects with the values put in the GUI
* Execute the transfer.
  * In pots spreadsheet:
    * Add a column, copy previous
    * Decrement the savings balance by the transfer amount
    * Adjust the pots based on the inputs
  * In the envelopes spreadsheet
    * Increase the total at the top
    * Adjust the envelopes based on the inputs

