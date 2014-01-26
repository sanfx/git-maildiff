from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import smtplib

class EMail(object):
		""" Class defines method to send email
		"""
		def __init__(self, mailFrom, server, usrname, password, files, debug=False):
				self.debug = debug
				self.mailFrom = mailFrom
				self.smtpserver = server
				self.EMAIL_PORT = 587
				self.usrname = usrname
				self.password = password


		def sendMessage(self, subject, msgContent, files, mailto):
			"""	Send the email message

				Args:
					subject(string): subject for the email
					msgContent(string): email message Content
					files(List): list of files to be attached
					mailto(string): email address to be sent to
			"""

			msg = self.prepareMail(subject, msgContent, files, mailto)

			# connect to server and send email
			server=smtplib.SMTP(self.smtpserver, port=self.EMAIL_PORT)
			server.ehlo()
			# use encrypted SSL mode
			server.starttls()
			# to make starttls work
			server.ehlo()
			server.login(self.usrname, self.password)
			server.set_debuglevel(self.debug)
			try:
				failed = server.sendmail(self.mailFrom, mailto, msg.as_string())
			except Exception as er:
				print er
			finally:
				server.quit()

		def prepareMail(self, subject, msgHTML, attachments, mailto):
			"""	Prepare the email to send
				Args:
					subject(string): subject of the email.
					msgHTML(string): HTML formatted email message Content.
					attachments(List): list of file paths to be attached with email. 
			"""
			msg = MIMEMultipart()
			msg['From'] = self.mailFrom
			msg['To'] = mailto
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject

			#the Body message
			msg.attach(MIMEText(msgHTML, 'html'))
			msg.attach(MIMEText("Sent using git ipush\n git clone https://sanfx@bitbucket.org/sanfx/git-ipush.git"))
			if attachments:
				for phile in attachments:
						# we could check for MIMETypes here
						part = MIMEBase('application',"octet-stream")
						part.set_payload(open(phile, "rb").read())
						Encoders.encode_base64(part)
						part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(phile))
						msg.attach(part)
			return msg
