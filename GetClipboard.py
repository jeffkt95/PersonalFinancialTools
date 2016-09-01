import win32clipboard

def main():
	print ("Hello world.")
	win32clipboard.OpenClipboard()
	fromClipboard = win32clipboard.GetClipboardData()
	win32clipboard.CloseClipboard
	print(fromClipboard)
	
	print("Yo yo!")
	#Your mom

if __name__ == "__main__":
	main()