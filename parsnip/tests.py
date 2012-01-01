from time import gmtime, strftime
from django.test import TestCase
from parsnip import get_webtexter, exceptions, utils

RECIPIENT_ONE = None
RECIPIENT_TWO = None
RECIPIENT_THREE = None

FAKE_NUM = "0811111111"
FAKE_PIN = "1111"

VODAFONE_NUM = None
VODAFONE_PIN = None
METEOR_NUM = None
METEOR_PIN = None
O2_NUM = None
O2_PIN = None
THREE_NUM = None
THREE_PIN = None

class TestUtils(TestCase):
	def chunk_string(self):
		# Breaking string into smaller strings
		self.assertEqual(utils.chunk("aa bb cc dd ee ff gg", 5), ['aa bb', ' cc d', 'd ee ', 'ff gg'])
		self.assertEqual(utils.chunk("aa bb", 5), ['aa bb',])
		self.assertEqual(utils.chunk("aa bb c", 5), ['aa bb',' c'])		
		self.assertNotEqual(utils.chunk("aa bb cc dd", 5), ['aa bb cc dd', ])
		
		# Using a webtext
		chunks = utils.chunk("This is a webtext that will be chunked into 8 smaller pieces of length 10", 10)
		self.assertEqual(len(chunks), 8)
		
	def chunk_list(self):
		# Breaking string into smaller strings
		self.assertEqual(utils.chunk(["1", "2", "3", "4", "5", "6"], 5), [["1", "2", "3", "4", "5",], ["6"]])
		self.assertEqual(utils.chunk(["1", "2", "3",], 1), [["1",], ["2"], ["3"]])
		self.assertEqual(utils.chunk(["1", "2", "3",], 3), [["1", "2", "3"],])
		
	def format_recipients_string(self):
		# String to list
		self.assertEqual(utils.csv_to_list("1, 2"), ["1", "2"])
		self.assertEqual(utils.csv_to_list("1"), ["1",])
		self.assertEqual(utils.csv_to_list("1, 2,,,"), ["1", "2", "", "", ""])
		
		self.assertEqual(utils.format_recipients_string("1, 2, 3 3, 444, , ,,,"), ["1", "33", '2', '444'])
		self.assertEqual(utils.format_recipients_string("1, 2, 33, ,4 4,5"), ['1', '33', '44', '2', '5'])
		self.assertEqual(utils.format_recipients_string(""), [])
		self.assertEqual(utils.format_recipients_string("1"), ["1"])
		self.assertEqual(utils.format_recipients_string("1,1,  1,, 1"), ["1"])
	
class TestNetworks(TestCase):
	"""
	To run these tests, you need to provide values for the variables above (number and pin's) for each 
	network. 
	
	WANRING!!
	
 	A lot (17) of webtexts will be sent every time this is run (to the three numbers above)
	"""
	def _do_tests(self, g, b):
		"""
		Test sending etc. when not logged in
		"""
		with self.assertRaises(exceptions.LoginError):
			# Try send message before logged in
			g.send("I'm trying to send while logged out", [RECIPIENT_ONE, ])
			b.send("I'm trying to send with incorrect details and while logged out", [RECIPIENT_ONE, ])
			# Try to get message count before logged in 
			g.get_remaining_webtexts()
			b.get_remaining_webtexts()
		
		"""
		Test good and bad normal logins
		"""
		self.assertTrue(g.login())
		self.assertRaises(exceptions.LoginError, b.login)
		
		
		"""
		Test validation (i.e. sending to zero recipients, or with a zero-length message)
		"""
		with self.assertRaises(AttributeError):
			# Try to send an empty message
			b.send(None, [RECIPIENT_ONE, ])
			b.send("", [RECIPIENT_ONE, ])
			b.send(1, [RECIPIENT_ONE, ])
			# Try to send an empty recipient list
			b.send("Lovely message", [])
			b.send("Lovely message", RECIPIENT_ONE)
		
		"""
		Test remainder messges
		"""
		self.assertIsInstance(g.get_remaining_webtexts(), int)
		
		"""
		Test message chunking. The MAX_LENGTH and MAX_RECIPIETS are reset here 
		"""
		g.MAX_LENGTH= 160
		g.MAX_RECIPIENTS = 2
		
		time = strftime("%H:%M:", gmtime())
		remaining = g.get_remaining_webtexts()
		
		#config = (False, False, False, False, False, False, False)
		config = (True, True, True, True, True, True, True)
		
		# 1.a Send normal sized message to single recipient
		if config[0]:
			self.assertTrue(g.send("1.a [%s] Single message to single recipient (list)" % time, [RECIPIENT_ONE, ]))
			self.assertEqual(remaining-1, g.get_remaining_webtexts())
			remaining = remaining-1
		
		# 1.b Send normal sized message to single recipient (as a string) (Should use 1 webtext)
		if config[1]:
			self.assertTrue(g.send("1.b [%s] Single message to single recipient (string)" % time, RECIPIENT_ONE))	
			self.assertEqual(remaining-1, g.get_remaining_webtexts())
			remaining = remaining-1
			
		# 2. Send normal sized message to 3 recipients (Should split the recipients in two lists and use 3 webtexts altogther)
		if config[2]:
			self.assertTrue(g.send("2. [%s] Single message to 3 recipients" % time, [RECIPIENT_ONE, RECIPIENT_TWO, RECIPIENT_THREE]))	
			self.assertEqual(remaining-3, g.get_remaining_webtexts())
			remaining = remaining-3
						
		# 3. Send long message to 3 recipients
		# Should:
		# - split the message into two string
		# - split the recipients into two lists 
		# - use two urllib requests to network
		# - use 6 webtexts altogether (2 msgs x 3 recipients)	
		if config[3]:
			self.assertTrue(g.send("""
				3. [%s] Long message to 3 recipients (~220 chars). It goes on and on and on and 
				on and on and on and on and on and on and on and on and on and on and on and on 
				and on and on and on and on and on and on and on and on """ % time, [RECIPIENT_ONE, RECIPIENT_TWO, RECIPIENT_THREE]))	
			self.assertEqual(remaining-6, g.get_remaining_webtexts())
			remaining = remaining-6
		
		# 4. Send normal message to 2 recipients (Should use two webtexts without and splitting of message or recipients)	
		if config[4]:
			self.assertTrue(g.send("4. [%s] Single message to 2 recipients" % time, [RECIPIENT_ONE, RECIPIENT_TWO]))	
			self.assertEqual(remaining-2, g.get_remaining_webtexts())
			remaining = remaining-2
			
		# 5. Send 3 single messages to single recipient in succession	
		if config[5]:
			self.assertTrue(g.send("5. [%s] Repeated Message 1" % time, [RECIPIENT_ONE]))	
			self.assertTrue(g.send("5. [%s] Repeated Message 2" % time, [RECIPIENT_ONE]))	
			self.assertTrue(g.send("5. [%s] Repeated Message 3" % time, [RECIPIENT_ONE]))	
			self.assertEqual(remaining-3, g.get_remaining_webtexts())
			remaining = remaining-3				
		
		# 6. Send normal sized message to list with duplicates (should only send once)		
		if config[6]:
			self.assertTrue(g.send("6 [%s] Single message to duplicate recipients (list)" % time, [RECIPIENT_ONE, RECIPIENT_ONE ]))
			self.assertEqual(remaining-1, g.get_remaining_webtexts())
			remaining = remaining-1
						
		"""
		Test logout and sending while logged out
		"""
		g.logout()
		with self.assertRaises(exceptions.LoginError):
			g.send("I'm trying to send while logged out", [RECIPIENT_ONE, ])
		
	def meteor(self):
		g = get_webtexter("Meteor", METEOR_NUM, METEOR_PIN)
		b = get_webtexter("Meteor", FAKE_NUM, FAKE_PIN)
		self._do_tests(g, b)
	
	def o2(self):
		g = get_webtexter("O2", O2_NUM, O2_PIN)
		b = get_webtexter("O2", FAKE_NUM, FAKE_PIN)
		self._do_tests(g, b)

	def three(self):
		g = get_webtexter("Three", THREE_NUM, THREE_PIN)
		b = get_webtexter("Three", FAKE_NUM, FAKE_PIN)
		self._do_tests(g, b)

	def vodafone(self):
		g = get_webtexter("Vodafone", VODAFONE_NUM, VODAFONE_PIN)
		b = get_webtexter("Vodafone", FAKE_NUM, FAKE_PIN)
		self._do_tests(g, b)