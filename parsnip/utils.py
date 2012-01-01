from sets import Set
import re

def make_string_safe(string):
	"""
	Decode 
	"""
	return string

def clean_list(l):
	"""Remove duplicates and empty entries from a list"""
	return list(Set(filter(None, l)))
	
def csv_to_list(s):
	"""Split commas separated string into a list (remove whitespace too)"""
	return [x for x in s.replace(" ", "").split(",")]
	
def format_recipients_string(string):
	"""
	Return a list with no dupes, no whitespace, and 
	no empty entries from a comma separated string
	"""
	return clean_list(csv_to_list(string))
	
def chunk(obj, max_length):
	"""
	A wrapped recursive function to chunk a list/string/... into pieces under a certain length/size,
	i.e. given a very long string, break it into numerous smaller strings, all under max_length:

	  $ result = utils.chunk(["aa bb cc dd ee ff gg", ], 0, 5)
	  $ ['aa bb', ' cc d', 'd ee ', 'ff gg']	
	
	or given a long list, break it into numerous smaller lists:

	  $ result = utils.chunk(["1", "2", "3", "4", "5", "6"], 0, 5)
	  $ [ ["1", "2", "3", "4", "5",], ["6", ] ]	
	"""
	def _c(l, i, max_length):
		while(len(l[i])>max_length):
			l.append((l[i])[max_length:])
			l[i] = (l[i])[:max_length]
			_c(l, i+1, max_length)
		return l
	return _c([obj, ], 0, max_length)