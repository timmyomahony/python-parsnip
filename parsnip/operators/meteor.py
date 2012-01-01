import re
import lxml.html
from lxml import etree
from urllib import urlencode

from parsnip import BaseWebtexter, exceptions

class Meteor(BaseWebtexter):
	
	NETWORK_NAME = "Meteor"
	LOGIN_PAGE = "https://www.mymeteor.ie"
	LOGIN_POST = "https://www.mymeteor.ie/go/mymeteor-login-manager"
	LOGOUT_POST = 'https://www.mymeteor.ie/go/logout'
	SEND_POST = 'https://www.mymeteor.ie/mymeteorapi/index.cfm'
	SEND_PAGE = 'https://www.mymeteor.ie/go/freewebtext'
	
	MAX_LENGTH = 480

	@classmethod
	def is_operator(cls, n):
		return n == cls.NETWORK_NAME
	
	def login(self):
		# Login
		response = self.connection.send(self.LOGIN_POST,data={
				'username' : self.phone_number,
				'userpass' : self.pin,
				'x' : '19',
				'y' : '13',
				'returnTo' : '/',
				})
		tree = lxml.html.fromstring(response)
		loginpage = tree.get_element_by_id("loginArea", None)
		if loginpage is not None:
			if tree.get_element_by_id("login-box-captcha", None) is not None:
				raise exceptions.LoginError("Too many invalid attempts, login on via meteor's website to reactivate your account", webtexter=self)
			for s in loginpage.iter("script"):
				if "Invalid login. Please try again" in s.text:
					raise exceptions.LoginError("Invalid Login Username or Pin", webtexter=self)
				elif "Your account is now timed out for 30 minutes. Please try again later" in s.text:
					raise exceptions.LoginError("Account has been timed out for 30 minutes", webtexter=self)
		elif tree.get_element_by_id("met-intro-panel", None) is not None:
			return True
		raise exceptions.LoginError("Unknown Login Error", webtexter=self)
				
	def _do_send(self, message_chunk, recipients_chunk):
		# Go to send page and check login
		response = self.connection.send(self.SEND_PAGE)
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("smsComposeTextArea", None)
		if smspage is None:
			if tree.get_element_by_id("login-box", None):
				raise exceptions.LoginError("Tried to send webtext while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error sending webtext", webtexter=self)
		# Add recipients via ajax
		for r in recipients_chunk:
			response = self.connection.send("%s?event=smsAjax&func=addEnteredMsisdns"%self.SEND_POST,data={
					'ajaxRequest':'addEnteredMSISDNs',
					'remove':'-',
					'add':"0|%s"%r})
			if not "appendRecipients(" in response:
				raise exceptions.MessageSendingError("Couldn't add recipient", webtexter=self)	
		# Do send
		response = self.connection.send("%s?event=smsAjax&func=sendSMS"%self.SEND_POST,data={
				'ajaxRequest':'sendSMS',
				'messageText':message_chunk,
				})
		if 'showEl("sentTrue");' in response:
			return True
		raise exceptions.MessageSendingError("Message not sent", webtexter=self)	
		
	def get_remaining_webtexts(self):
		# Go to send page
		response = self.connection.send(self.SEND_PAGE)
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("smsComposeTextArea", None)
		if smspage is None:
			if tree.get_element_by_id("login-box", None):
				raise exceptions.LoginError("Tried to get webtext count while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error retrieving webtext count", webtexter=self)
		# Get remaining texts
		r = tree.get_element_by_id("numfreesmstext", None)
	 	return int(r.attrib.get('value'))
