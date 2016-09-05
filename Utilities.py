import datetime
import win32clipboard

def reverseSign(value):
    #Remove commas. Comma delimiters screw up casting as float.
    strWithoutCommas = value.replace(",", "")
    if (is_number(strWithoutCommas)):
        return -1 * float(strWithoutCommas)
    else:
        return value

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
  
def isDate(possibleDate):
    try:
        datetime.datetime.strptime(possibleDate, '%m/%d/%Y')
        return True
    except ValueError:
        return False

def getClipboard():
    #TODO: gracefully handle an empty clipboard
    win32clipboard.OpenClipboard()
    fromClipboard = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard
    return fromClipboard
    
def print_data2(values):
    for i in range(len(values)):
        rowString = " "
        for j in range(len(values[i])):
            rowString = rowString +  "   " + str(values[i][j])
        print(rowString)

def print_data1(values):
    for value in values:
        print("'" + str(value) + "'")

def print_data(values):
    if not values:
        print('No data found.')
    else:
        print('Envelope name, Amount, Amount spent, Amount left, %spent')
        for row in values:
            # Print columns A, B, C, D, E
            if (len(row) >= 5):
                print('%s, %s, %s, %s, %s' % (row[0], row[1], row[2], row[3], row[4]))
