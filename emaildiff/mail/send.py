from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders
import os
import socket
import smtplib

class EMail(object):
	""" Class defines method to send email
	"""
	def __init__(self, mailfrom, server, usrname, password, logger, debug=False):
		self.debug = debug
		self._log = logger
		self.mailFrom = mailfrom
		self.smtpserver = server
		self.EMAIL_PORT = 587
		self.usrname = usrname
		self.password = password


	def sendMessage(self, subject, msgContent, files, mailto):
		"""	Send the email message

			:param subject: subject for the email
			:type subject: str

			:param msgContent: email message Content
			:type msgContent: str

			:param files: list of files to be attached
			:type files: list

			:param mailto: email address to be sent to
			:type mailto: str
		"""

		msg = self.prepareMail(subject, msgContent, files, mailto)
		try:
			# connect to server and send email
			server = smtplib.SMTP(self.smtpserver, port=self.EMAIL_PORT)
			server.ehlo()
		except socket.gaierror as err:
			self._log.error(err)
		else:
			# use encrypted SSL mode
			server.starttls()
			# to make starttls work
			server.ehlo()
			server.login(self.usrname, self.password)
			server.set_debuglevel(self.debug)
			try:
				server.sendmail(self.mailFrom, mailto, msg.as_string())
			except Exception as er:
				print er
				return False
			finally:
				server.quit()
			return True

	def prepareMail(self, subject, msgHTML, attachments, mailto):
		"""	Prepare the email to send

			:param subject: subject of the email.
			:type subject: str

			:param msgHTML: HTML formatted email message Content.
			:type msgHTML: str

			:param attachments: list of file paths to be attached with email.
			:type attachments: list

			:Returns msg: message to be sent
			:type msg: str
		"""
		msg = MIMEMultipart()
		msg['From'] = self.mailFrom
		msg['To'] = mailto
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = subject

		#the Body message
		msg.attach(MIMEText(msgHTML, 'html'))
		for phile in attachments:
			# we could check for MIMETypes here
			part = MIMEBase('application', "octet-stream")
			part.set_payload(open(phile, "rb").read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(phile))
			msg.attach(part)
		return msg
