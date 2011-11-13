from settings import meteor as settings
from base import Webtexter

from BeautifulSoup import BeautifulSoup

import urllib,urllib2,cookielib

class MeteorWebtexter(Webtexter):
	
	def __init__(self,number,pin):
		super(MeteorWebtexter,self).__init__(number,pin)
		
	def sendText(self, message, recipients):
		if self.logged_in:
			if isinstance(recipients,list):	
				# Change recipient list into string for meteor
				recipients_str = ''
				try:
					recipients_str = "111111|%s|no one"%('|'.join(str(n) for n in recipients))
				except:
					return {"sent" : False,"message" : "Couldn't encode recipients"} 
		
				# First tell meteor to add recipients via ajax
				super(MeteorWebtexter,self)._send(
					settings.SEND_POST_URL,	
					urllib.urlencode({
						'event':'smsAjax',
						'func':'addEnteredMsisdns',
						'ajaxRequest':'addEnteredMSISDNs',
						'remove':'-',
						'add':recipients_str,
					})
				)
			
				# Now send the message to those recipients
				reply = super(MeteorWebtexter,self)._send(
					settings.SEND_POST_URL,	
					urllib.urlencode({
						'event':'smsAjax',
						'func':'sendSMS',
						'ajaxRequest':'sendSMS',
						'messageText':message,
					})
				)
				
				# Check reply
				if "Sending SMS Message</h2>" in reply or 'showEl("sentTrue");' in reply:
					return {"status" : "Message Sent"}
				elif "MyMeteor customer log" in reply:
					return {"err" : "Not Logged In"}
				else:
					return {"err" : "Unknown Error"}
			else:
				return {"err" : "Recipients must be a list"}
		else:
			return {"err": "Not Logged In"}
			
	def login(self):
		reply = super(MeteorWebtexter,self)._send(
			settings.LOGIN_POST_URL,
			urllib.urlencode({
				'username':self.number,
				'userpass':self.pin,
				'x':'19',
				'y':'13',
				'returnTo':'/',
			})
		)
		if "My Account</h3>" in reply:
			self.logged_in = True
			return {"status" : "Login Successful"}
		else:
			self.logged_in = False	
		if "Invalid login. Please try again" in reply:
			return {"err" : "Invalid Login"}
		elif "captcha_value" in reply:
			return {"err" : "Too Many Attempts"}
		else:
			return {"err" : "Unknown Error"	}
			
	def logout(self):
		super(MeteorWebtexter,self)._send("https://www.mymeteor.ie/go/logout")
		super(MeteorWebtexter,self).logout()
		
	def checkLogin(self):
		return super(MeteorWebtexter,self).checkLogin(self)
	
	def getMessageCount(self):
		if self.logged_in:
			reply = super(MeteorWebtexter,self)._send("https://www.mymeteor.ie/go/freewebtext")
			tree = BeautifulSoup(reply)
			try:
				return tree.find(id='numfreesmstext')['value']
			except:
				return -1
		else:
			return -1