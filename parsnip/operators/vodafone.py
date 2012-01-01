from parsnip import BaseWebtexter, BaseConnection, exceptions
import urllib,urllib2,cookielib, re
import time
import sys
import lxml.html
from lxml import etree
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup										  

class Vodafone(BaseWebtexter):
	
	NETWORK_NAME = "Vodafone"
	LOGIN_POST = 'https://www.vodafone.ie/myv/services/login/Login.shtml'
	LOGOUT_POST = "https://www.vodafone.ie/myv/services/logout/Logout.shtml"
	SEND_POST = "https://www.vodafone.ie/myv/messaging/webtext/Process.shtml"
	SEND_PAGE = "https://www.vodafone.ie/myv/messaging/webtext/index.jsp"
		   
	MAX_LENGTH = 480
	MAX_RECIPIENTS = 5

	@classmethod
	def is_operator(cls, n):
			return n == cls.NETWORK_NAME
					
	def login(self):
		#Check login
		response = self.connection.send(self.LOGIN_POST,{
						'username' : self.phone_number,
						'password' : self.pin })
		tree = lxml.html.fromstring(response)
		loginpage = tree.get_element_by_id("mobile_number", None)
		if loginpage is not None:
			errorbox = tree.find_class('error-msg-box')
			if len(errorbox) > 0:
					error = errorbox[0].find('ul')
					if "Your mobile number and password do not match" or "Your mobile number is not valid" in error.text_contents():
							raise exceptions.LoginError("Invalid Login Username or Pin", webtexter=self)
			raise exceptions.LoginError("Unknown Login Error", webtexter=self)
		return True
				
	def _do_send(self, message_chunk, recipients_chunk):
		# Go to send page and check login
		response = self.connection.send(self.SEND_PAGE) 
		time.sleep(2)
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("message", None)
		if smspage is None:
			if tree.get_element_by_id("top-register-btn", None):
				raise exceptions.LoginError("Tried to send webtext while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error sending webtext", webtexter=self)
		# Append dummy empty recipients
		for i in range(5-len(recipients_chunk)):
			recipients_chunk.append(u"")
		# First get Apache Token
		tree = BeautifulSoup(response)
		token = ""
		token = str(tree.find('input',attrs={'name':'org.apache.struts.taglib.html.TOKEN'})['value'])
		send_data = {
				"org.apache.struts.taglib.html.TOKEN":token,
				"message":message_chunk,
				"sendnow":"Send+Now",
				"futuredate":"false",
				"futuretime":"false",
				}		
		# Add recipients
		for i,r in enumerate(recipients_chunk):
			send_data['recipients[%s]'%i] = str(r)
		# Send
		response = self.connection.send(self.SEND_POST, send_data)
		tree = lxml.html.fromstring(response)
		sendpage = tree.get_element_by_id('webtext-thankyou', None)
		if sendpage is not None and "Message sent!" in sendpage.text_content():
				return True
		raise exceptions.MessageSendingError("Message not sent", webtexter=self)	
		
	def get_remaining_webtexts(self):
		# Go to send page and check login
		response = self.connection.send(self.SEND_PAGE) 
		time.sleep(2)
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("message", None)
		if smspage is None:
			if tree.get_element_by_id("mobile_number", None):
				raise exceptions.LoginError("Tried to send webtext while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error sending webtext", webtexter=self)
		# Get the number of message left
		c = tree.get_element_by_id("content-pane")
	 	return int((c.find_class("text-remaining")[0]).find("strong").text)
