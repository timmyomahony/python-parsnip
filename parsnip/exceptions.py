class ParsnipException(Exception):
	
	def __init__(self, msg, webtexter=None):
		self.args = (msg, webtexter)
		self.msg = msg
		self.webtexter = webtexter
		
	def __str__(self):
		return repr("[%s] %s - %s" % (self.webtexter.NETWORK_NAME, self.webtexter.phone_number, self.msg))
		
class LoginError(ParsnipException):pass
class MessageSendingError(ParsnipException):pass
class ConnectionError(ParsnipException):pass		
class ResourceError(ParsnipException):pass

