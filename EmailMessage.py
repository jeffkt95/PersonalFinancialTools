import sys
import smtplib
import email
import email.mime.text
import email.mime.multipart
import os

class EmailMessage:
	"""
	This class is used to build an email message with an attachment, and then send it.
	"""

	def __init__(self, smtpServerUrl, fromAddress, subject, username, password):
		self.smtpServerUrl = smtpServerUrl
		
		self.message = email.mime.multipart.MIMEMultipart()
		self.message['Subject'] = subject
		self.message['From'] = fromAddress
		self.username = username
		self.password = password

	def addPlainTextBody(self, body):
		messageBody = email.mime.text.MIMEText(body)
		self.message.attach(messageBody)

	def addHtmlBody(self, body):
		messageBody = email.mime.text.MIMEText(body, 'html')
		self.message.attach(messageBody)

	def addAttachment(self, attachmentMimeType, attachmentMimeSubtype, fileToAttachPath):
		fileToAttach = open(fileToAttachPath, 'rb')
		fileMsg = email.mime.base.MIMEBase(attachmentMimeType, attachmentMimeType)
		fileMsg.set_payload(fileToAttach.read())
		email.encoders.encode_base64(fileMsg)
		fileMsg.add_header('Content-Disposition','attachment;filename=' + os.path.basename(fileToAttachPath))
		self.message.attach(fileMsg)
		
	def addReplyTo(self, replyToAddresses):
		self.message.add_header('reply-to', replyToAddresses)
	
	def send(self, toAddresses, ccAddresses):
		self.message['To'] = toAddresses
		self.message['Cc'] = ccAddresses
	
		server = smtplib.SMTP(self.smtpServerUrl)
		server.ehlo()
		server.starttls()
		server.set_debuglevel(0)
		server.login(self.username, self.password)
		server.sendmail(self.message['From'], toAddresses.split(';') + ccAddresses.split(';'), self.message.as_string())
		server.quit()
	
def main(argv):
	toAddresses = "jeffkt95@gmail.com"
	ccAddresses = "jeffkt95@gmail.com"
	
	messageBody = "Test message body.\r\n\r\n"
	messageBody = messageBody + "Thanks,\r\nJeff\r\n"
	
	#fileWithHtmlBody = open("../daily_status_automation/dailyStatusTemplate.txt", 'rb')
	#messageBodyHtml = fileWithHtmlBody.read()
	
	emailMessage = EmailMessage('smtp.gmail.com:587', 'jeffkt95@gmail.com', 'Test email subject', 'jeffkt95@gmail.com', 'WRONG_PASSWORD')
	emailMessage.addPlainTextBody(messageBody)
	#emailMessage.addHtmlBody(messageBodyHtml)
	emailMessage.addReplyTo('jeffkt95@gmail.com')
	#emailMessage.addAttachment('application', 'vnd.ms-excel', 'c:/mydata/temp/ara_jira_export.xls')
		
	emailMessage.send(toAddresses, ccAddresses)


if __name__ == "__main__":
	main(sys.argv[0])
