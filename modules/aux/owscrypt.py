class owscrypt:


	def __init__(self, framework):

		self.name = "owscrypt"
		self.description = "OWS Cryptography Framework"
		self.fw = framework
		self.variables = {}
		self.variables['mode'] = {'required' : True, 'description' : "Mode to use from Crypt Library"}
		self.variables['file'] = {'required' : False, 'description' : "File to Apply Crypt Lib Method to.", 'default' : 'None'}
		self.variables['key'] = {'required' : False, 'description' : "Key for encryptions, only needed for select few.", 'default' : 'None' }
		
	def loadModule(self):

		return True

	def installModule(self):

		return True

	def check(self):

		return True

	def exploit(self):
		if self.mode == "reverse":
			self.fw.libs.crypt.rev(self.file)
		elif self.mode == "caesar":
			self.fw.libs.crypt.caesar(self.file, self.key)
		return True