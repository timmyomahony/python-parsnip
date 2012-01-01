from parsnip import BaseWebtexter, exceptions
import lxml.html
from lxml import etree
import urllib

class O2(BaseWebtexter):

	NETWORK_NAME = "O2"
	LOGIN_POST = 'https://www.o2online.ie/amserver/UI/Login/'
	LOGOUT_POST = "http://www.o2online.ie/wps/wcm/connect/O2/Logged+Out/LogoutPage"
	SEND_POST = 'https://messaging.o2online.ie/smscenter_send.osp'
	SEND_PAGE = None

	MAX_LENGTH = 1000		# 15 texts
			
	@classmethod
	def is_operator(cls, n):
		return n == cls.NETWORK_NAME
	
	def login(self):
		response = self.connection.send(self.LOGIN_POST,data={
				'IDToken1':self.phone_number,
				'IDToken2':self.pin,
				'org':'o2ext',
				})
		tree = lxml.html.fromstring(response)
		loginpage = tree.get_element_by_id("LoginBox", None)
		if loginpage is not None:
			errorbox = tree.get_element_by_id("errorBlock", None)
			if errorbox is not None:
				for s in errorbox.iter("p"):
					if "Your login has been unsuccessful due to in-correct details." in s.text:
						raise exceptions.LoginError(msg="Invalid Login Username or Pin", webtexter=self)
			raise exceptions.LoginError("Unknown Login Error", webtexter=self)
		return True
			
	def _do_send(self, message_chunk, recipients_chunk):
		# Go to send page and check login
		self.connection.send('http://messaging.o2online.ie/ssomanager.osp?APIID=AUTH-WEBSSO')
		response = self.connection.send('http://messaging.o2online.ie/o2om_smscenter_new.osp?SID=59326281_okhohbof&REF=1304873573&MsgContentID=-1')
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("txtA_SMSMessage", None)
		if smspage is None:
			if tree.get_element_by_id("LoginBox", None):
				raise exceptions.LoginError("Tried to send webtext while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error sending webtext", webtexter=self)
		# Send Message
		response = self.connection.send("http://messaging.o2online.ie/smscenter_send.osp", data={
			"SMSTo":(','.join(str(n) for n in recipients_chunk)),
			'SMSText': message_chunk,
			"SID":"70285502_azmiemoc",
			"FlagDLR":"1",
			"RepeatStartDate":"2011,10,07,17,45,00",
			"RepeatEndDate":"2011,10,07,17,45,00",
			"RepeatEndType":"0",
			"RepeatType":"0",
			"FolderID":"0",
			"REF":"1318005011",
			"RURL":"asp_getfileid.osp?SID=70285502_azmiemoc&FID=6422",			  
		})
		if "isSuccess : true" in response:
			return True
		raise exceptions.MessageSendingError("Message not sent", webtexter=self)
		
	def get_remaining_webtexts(self):
		# Go to send page
		self.connection.send('http://messaging.o2online.ie/ssomanager.osp?APIID=AUTH-WEBSSO')
		response = self.connection.send('http://messaging.o2online.ie/o2om_smscenter_new.osp?SID=59326281_okhohbof&REF=1304873573&MsgContentID=-1')
		# Check if logged in
		tree = lxml.html.fromstring(response)
		smspage = tree.get_element_by_id("txtA_SMSMessage", None)
		if smspage is None:
			if tree.get_element_by_id("LoginBox", None):
				raise exceptions.LoginError("Tried to get webtext count while not logged in", webtexter=self)
			raise exceptions.MessageSendingError("Unknown error retrieving webtext count", webtexter=self)
		# Get remaining texts
		tree = lxml.html.fromstring(response)
 		return int(tree.get_element_by_id("spn_WebtextFree", None).text)