import sys
import glob
import os

class libraries:

	def __init__(self, framework):

		#self.framework = framework
		self.framework = framework
		self._liblist = self.preloadLibs()
		for lib in self._liblist:
			if '__init__' in lib or '.pyc' in lib:
				continue

	# Create an instance of the library
	def loadLibrary(self, lib):

		if lib == "libs." or "__init__" in lib or ".pyc" in lib:
			return False
		libf = "libs."+str(lib)
		if not os.path.isfile("libs/"+lib+".py"):
			print self.framework.prompt + " " + libf + " is not a valid library"
			return False
		#print self.framework.prompt+" Loading Library " + lib
		library = self.ezImport(libf)
		setattr(self, str(lib), library(self.framework))

	# Import Library
	def ezImport(self, name):
		components = name.split('.')
		comp = components[1]
		mod = __import__(name, fromlist=[comp])
		mod = getattr(mod, comp)
		return mod

		# Load modules into global namespace
	def preloadLibs(self):

		sys.path.append("libs")
		lib = glob.glob("libs/*.py")
		lib_files = []
		for i in range(len(lib)):
			self.loadLibrary(lib[i][5:-3])
			lib[i] = lib[i].split(".")[0].split("/")[1]
			lib[i] = "libs."+lib[i]
			globals()[lib[i]] = self.ezImport(lib[i])
			lib_files.append(lib[i])

		return lib_files

	# List installed libraries
	def listLibs(self):

		classes = glob.glob("libs/*.py")
		for i in range(len(classes)):
			classes[i] = classes[i].split(".")[0].split("/")[1]
			if classes[i] == '__init__':
				continue
			classes[i] = "libs."+classes[i]
			if classes[i] in globals():
				lib = self.ezImport(classes[i])
				library = lib(self)
				print self.framework.prompt+self.framework.libs.colours.cstring(' ~> ', 'white')+self.framework.libs.colours.cstring(library.name+" - "+library.description, "blue")
				library = None

		return True