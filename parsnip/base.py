from settings import common

import random
import os
import urllib
import urllib2
import cookielib
	
class Webtexter(object):
	"""
		Basically an interface to suggest what methods a webtexter should 
		supply
	"""
	def __init__(self,number,pin):
		self.logged_in = False
		self.number = number
		self.pin = pin
		self.cookiejar = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
	
	def _validMessage(self, message):
		"""
			Check whether a message is valid according to the operators
			guidelines
		"""
		pass
		
	def _validNumber(self, number):
		"""
			Check whether a recipientsnumber is valid according to the 
			operators POST guidelines
		"""
		pass
		
	def _send(self,url, data=None):
		"""
			Perform actual POST or GET
		"""
		try:
			request = urllib2.Request(url,data,{
				'User-agent': random.choice(common.UAS)
			})
			response = self.opener.open(request)
		except IOError, err:
			if hasattr(err, 'code'):
				print "Code:%s"% err.code
		else:
			return response.read()
			
	def sendText(self, message, recipients):
		"""
			Send a message
		"""	
		pass
		
	def login(self):
		"""
			Perform login
		"""
		pass		
		
	def logout(self):
		"""
			
		"""
		try:
			self.cookiejar.clear()
		except:
			pass
		self.logged_in = False
		
	def checkLogin(self):
		"""
			
		"""
		pass
		
	def getMessageCount(self):
		"""
			Get the message count for this account
		"""
		pass