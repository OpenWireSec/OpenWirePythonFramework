import random

class text:

	def __init__(self, framework):
		
		self.fw = framework
		self.formattedString = ""
		self.specialchars = [" ", ",", "@", "#", "$", "%", "^", "&", "=","[", "]", "-", "{", "}", "\\", "/", "*", "!", ".", "_", "(", ")", "+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
		self.name = "Text"
		self.description = "Library to provide generic text manipulation and encoding functions"


	"""
		warpText(string)

		randomly capitalizes strings to attempt WAF evasion
	"""
	def warpText(self, string):

		self.formattedString = ""
		string = string.replace("\n", "")
		while string[len(string)-1] == " ": string = string[:-1]
		while string[0] == " ": string = string[1:]

		sentence = string.split(" ")

		for i in range(len(sentence)):
			spc_char = None
			unique = 0
			while unique == 0:
				obfWord = ""
				for x in range(len(sentence[i])):
					spc_char = 0

					if sentence[i][x] in self.specialchars:
						obfWord += sentence[i][x]
						spc_char = 1
						continue

					cap = random.randint(0,1)
					if cap:
						obfWord += sentence[i][x].upper()
					else:
						obfWord += sentence[i][x].lower()
				if len(obfWord) == 1 or (obfWord != sentence[i].lower() and obfWord != sentence[i].upper()) or spc_char == 1:
					unique = 1
					self.formattedString += obfWord + " "
		return self.formattedString[:-1]
	"""
	strHex($string)
	converts $string to its hex value
	"""
	def strHex(self, string):

		self.formattedString = ""
		self.formattedString = string.encode("hex").replace("\n", "")

		return self.formattedString

	"""
	hexStr($string)
	converts the hex $string to its decimal equivalent, converts to char, and appends to a string.
	"""
	def hexStr(self, string):

		self.formattedString = ""
		self.formattedString = string.decode("hex").replace("\n", "")

		return self.formattedString

		"""
	strRot13($string)
	converts $string to its rot13 value
	"""
	def strRot13(self, string):

		return self.rot13(string)

	"""
	rot13Str($string)
	converts the rot13 $string to plaintext
	"""
	def rot13Str(self, string):

		return self.rot13(string)

	def rot13(self, string):

		return string.encode("rot13").replace("\n", "")

	"""
	strBase64($string)
	converts $string to its base64_encode value
	"""
	def strBase64(self, string):

		self.formattedString = ""
		self.formattedString = string.encode("base64").replace("\n", "")

		return self.formattedString

	"""
	base64Str($string)
	converts the base64 $string to plaintext
	"""
	def base64Str(self, string):

		self.formattedString = ""
		self.formattedString = string.decode("base64").replace("\n", "")

		return self.formattedString


	"""
	strOct($string)
	converts $string to its oct value
	"""
	def strOct(self, string):
		return False
	def octStr(self, string):
		return False

	def sqlSpace(self, string):

		self.formattedString = ""

		self.formattedString = string.replace(" ", "/**/").replace("+", "/**/").replace("\n", "")
		
		return self.formattedString
