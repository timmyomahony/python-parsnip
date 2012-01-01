import urllib
import urllib2
import cookielib
from lxml import etree

DEBUG = False
VERSION = "0.0.1"

import logging
logger = logging.getLogger(__name__)
if DEBUG:
	logging.basicConfig(level=logging.DEBUG)

class Webtext(object):
	"""
	Represents a webtext to be sent to a list of recipients. It does some simple
	validation and formatting on the provided message and recipients. 
	"""
	def __init__(self, message, recipients):
		if not isinstance(message, str):
			raise AttributeError("The message must be a string")
		else:
			if len(message) is 0:
				raise AttributeError("The message string provided was empty")	
		self.message = utils.make_string_safe(message)
		if not isinstance(recipients, list):
			try:
				recipients = utils.csv_to_list(recipients)
			except:
				raise AttributeError("Provided recipients were not in a list and could not be converted.")
		recipients = utils.clean_list(recipients)
		if len(recipients) is 0:
			raise AttributeError("No recipients in the list")
		self.recipients = recipients
							
class BaseConnection(object):
		"""
		A wrapper around URLLib concerned with the sending & receiving of messages to the mobile operators 
		websites. Also responsible for the managing of cookies.
		"""
		def __init__(self):
			self.cookies = cookielib.CookieJar()
			self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookies))
		
		def send(self,url, data=None, headers=None):
			""" 
			"""
			if data:
				data = urllib.urlencode(data)
			if not headers:
				headers = {
					"Referer":"http://www.google.com",
					"Content-type": "application/x-www-form-urlencoded",
					"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
					"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0) Gecko/20100101 Firefox/4.0"
					}
			request = urllib2.Request(url=url, data=data, headers=headers)
			return self.opener.open(request).read()
						
class BaseWebtexter(object):
		""" """
		
		MAX_LENGTH = 128	
		MAX_RECIPIENTS = 24
		
		def __init__(self, phone_number, pin, *args, **kwargs):
			self.phone_number = phone_number
			self.pin = pin
			self.remaining_webtexts = None
			self.connection = BaseConnection()	
			
		def login(self):
			raise NotImplementedError()
			
		def logout(self):
			if self.LOGOUT_POST:
				self.connection.send(self.LOGOUT_POST)
			self.connection.cookies.clear()
				
		def _do_send(self, message_chunk, recipient_list_chunk):
			"""
			This should be overwritten to provide the actual network specific logic for sending a single message. 
			
			Parameters:
			- message_chunk : is a string that is less then `self.MAX_LENGTH` chars
			- recipient_list_chunk : is a list with less then `self.MAX_RECIPIENTS` entries
			"""
			raise NotImplementedError()
				
		def send(self, message, recipients):
			"""
			Front-facing sending wrapper to send a message to a list (or comma separated string) of phone numbers. This 
			method automatically breaks the message and recipient list into smaller chunks if they are bigger then the
			network provider can deal with (depending on what has been set in self.MAX_LENGTH and self.MAX_RECIPIENTS)
			
			Parameters:
			- message : a string of any length 
			- recipients : a comma separated string or a list of strings containing the phone numbers to send to. 
			"""	
			webtext = Webtext(message, recipients)
			for message_chunk in utils.chunk(webtext.message, self.MAX_LENGTH):
				for recipient_chunk in utils.chunk(webtext.recipients, self.MAX_RECIPIENTS):
					self._do_send(message_chunk, recipient_chunk)	
			return True					
			
		def get_remaining_webtexts(self):
			raise NotImplementedError()	

		def __unicode__(self):
			return u"%s-%s" %(self.is_operator, self.phone_number)
				
		def __str__(self):
			return u"%s-%s" %(self.is_operator, self.phone_number)
				
import operators				
def get_webtexter(network_name, phone_number, pin):
	"""
	Factory function to create webtexters given a string representing the operator (e.g. 'Meteor'/'O2')
	"""
	for cls in BaseWebtexter.__subclasses__():
		if cls.is_operator(unicode(network_name)):
			return cls(phone_number, pin)
	raise ValueError, "Webtexter for %s has not been implemented" % network_name
