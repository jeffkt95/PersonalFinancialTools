import win32clipboard

#TODO: consider making this a class

def main():
	print ("Hello world.")
	win32clipboard.OpenClipboard()
	fromClipboard = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard
	print(fromClipboard)
	
if __name__ == "__main__":
	main()