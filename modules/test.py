import socket

class test:

	def __init__(self, framework):
		
		self.name = "Test"
		self.description = "A test module for the python framework"
		self.framework = framework
		self.variables = {}
		self.variables['message'] = {'required' : False, 'description' : 'String to modify', 'default' : 'This is a test string'}

	def loadModule(self):

		return True

	def installModule(self):

		return True

	def check(self):

		print self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("*","red")+self.framework.libs.colours.cstring("] ", "green")+"This module does not support check"

		return True

	def exploit(self):

		self.test()

		return True

	def post(self):

		print "This module does not support Post Exploit"

		return True

	def test(self):
		string = "This is a test string"
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+self.framework.libs.text.warpText(string)

		test = "Checking " + self.target

		hexstr = self.framework.libs.text.strHex(test)
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+hexstr
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+"And back again: " + self.framework.libs.text.hexStr(hexstr)

		base64 = self.framework.libs.text.strBase64(test)
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+base64
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+"And back again: " + self.framework.libs.text.base64Str(base64)

		rot13 = self.framework.libs.text.strRot13(test)
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+rot13
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+"And back again: " + self.framework.libs.text.rot13Str(rot13)	

		spaces = "This is a test+string+with+several different types+of+spaces"	
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+spaces
		print "\t"+self.framework.libs.colours.cstring("[", "green")+self.framework.libs.colours.cstring("+","blue")+self.framework.libs.colours.cstring("] ", "green")+self.framework.libs.text.sqlSpace(spaces)


		

		return True
