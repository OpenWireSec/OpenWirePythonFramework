from lib import *
import HTTPThread
import completer
import readline
import Queue
import math
import time
import glob
import sys
import os

"""
openWire Python Framework
Design based on 0x0F php Framework
By: Phaedrus
Date: March 2, 2013

A basic exploitation framework, can dynamically load modules and libraries
includes a builtin multithreaded HTTP Handler 
"""
class Framework:

	def __init__(self):
		self.libs = libraries(self)
		self.time = time.time()
		self.module = None
		self.prompt = "openWire"
		self.threads = 10
		self.queries = 0
		self.modType = None
		self.regexURL = "#^(https?://)?[a-zA-Z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$#"
		self.framework = self
		self.variables = {}
		self.useragent = "Mozilla/5.0 (X11 Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/10.04 Chromium/17.0.963.56 Chrome/17.0.963.56 Safari/535.11"
		self.regexPath = "#^[a-zA-Z0-9\.\-_~\!\$&\'\(\)\*\+,\=\:@/]+$#"
		self.threadArray = []
		self.defaultVariables = {'target' : {'required' : True, 'description' : 'The target host (ex. www.google.com)'}}
		self.autocomp = ['use', 'view', 'load', 'run', 'exploit', 'check', 'show', 'variables', 'set', 'help', 'list', 'libs', 'clear', 'cls', 'banner', 'exit', 'stop', 'quit']

	def run(self):
		#preload libraries
		self.preloadModules()
		self.outputHeader()
		
		
		# Define escape commands
		exitCommands = ['quit', 'exit', 'stop']

		# Register our completer function
		self.genList()
		readline.set_completer(completer.completer(self.autocomp).complete)

		# Use the tab key for completion
		readline.parse_and_bind('tab: complete')

		# Initialize Input Container
		line = ""

		# Receive user input
		while line not in exitCommands:

			# Set the prompt 
			if self.module != None:
				self.prompt = self.libs.colours.cstring('(', 'red')+self.libs.colours.cstring("openWire", 'light_blue')+self.libs.colours.cstring("->", "red") + self.libs.colours.cstring(self.module.name, "white")+self.libs.colours.cstring(')', 'red')
			else:
				self.prompt = self.libs.colours.cstring('(', 'red')+self.libs.colours.cstring("openWire", 'light_blue')+self.libs.colours.cstring(')', 'red')
			
			# Read user input
			sys.stdout.write(self.prompt)
			sys.stdout.write(' ') 
			line = raw_input()
			
			# Parse user input
			if line == "" or line in exitCommands:
				continue

			self.parseInput(line)

	def parseInput(self, line):

			commands = line.split(" ")

			# Parse user Input

			# Print Help Message
			if commands[0] == 'help':
				self.showUsage()
			

			# List available Modules
			elif commands[0] == 'list':
				self.listModules()

			# Unload currently selected module
			elif commands[0] == 'back':
				self.module = None
				
			# Load a module
			elif commands[0] == 'use' or commands[0] == 'load':
			
				if len(commands) < 2:
					self.showUsage()
					return False
				self.loadModule(commands[1].lower())
			
			# Set current modules variables
			elif commands[0] == 'set':
			
				if len(commands) < 3:
					self.showUsage()
					return False
				self.setValue(commands[1], ' '.join(commands[2:]))
			

			# show current modules variables
			elif commands[0] == 'show':
			
				if commands[1] == 'variables':
					self.showVariables()
				else:
					self.showUsage()

			# show current modules variables
			elif commands[0] == 'view':
				
				self.showVariables()
			
			#List installed libraries
			elif commands[0] == 'libs':
				
				self.libs.listLibs()
			
			# Check if target is vulnerable to current module(not available in auxiliary modules)
			elif commands[0] == 'check':

				self.checkExploit()

			# Print the current time to the terminal
			elif commands[0] == 'time':

				self.printTime()
			
			# Begin Module Execution
			elif commands[0] == 'run' or commands[0] == 'exploit':
				
				self.runExploit()
			
			# Clear the terminal output
			elif commands[0] == 'clear' or commands[0] == 'cls':
				
				self.clearScreen()
			
			# Clear the terminal output and print a banner
			elif commands[0] == 'banner':
				self.outputHeader()

			# Disable HAL-9000 Higher Function Modules
			elif commands[0] == 'pewpew':
				self.hal(1)

			# Try to kill HAL-9000 system
			elif commands[0] == 'die':
				self.hal()

			# Handle incorrect input
			else:
				print self.prompt+self.libs.colours.cstring(' ~> ', 'white'), 
				print "%s is not a valid command" % commands[0]

	# Print banner
	def outputHeader(self):

		self.clearScreen()
   
		print
		print "  _|_|                                  _|          _|  _|                     "
		print "_|    _|  _|_|_|      _|_|    _|_|_|    _|          _|      _|  _|_|    _|_|   "
		print "_|    _|  _|    _|  _|_|_|_|  _|    _|  _|    _|    _|  _|  _|_|      _|_|_|_| "
		print "_|    _|  _|    _|  _|        _|    _|    _|  _|  _|    _|  _|        _|       "
		print "  _|_|    _|_|_|      _|_|_|  _|    _|      _|  _|      _|  _|          _|_|_| "
		print "          _|                                                                   "
		print "          _|                                                                  \n"
		print "                           ~ 0-day Framework ~            \n"
    
		return True

	# Print Help Message
	def showUsage(self):

		print self.libs.colours.cstring("""
	OpenWire 0-day Framework, version 1.0-stable
	List of commands and description of usage""", "light_gray")
   
		print self.libs.colours.cstring("""
	\thelp - Display this list
	\tclear/cls - Clears the Screen
	\tlibs - List current libraries
	\tbanner - Displays the Banner
	\tlist - List current exploit modules
	\ttime - Displays the current system time
	\tdie - Defuse HAL-9000 System
   
	\tuse/load <exploit> - Load an exploit module
	\tback - Unloads current module
	\tset <variable> <value> - Set a variable to value (ex. target host)
	\tshow variables - Show the global and exploit specific variables
	\tview - Show currently set variable values
	\tcheck - Check if the target is vulnerable to currently loaded exploit
	\texploit - Run the currently loaded exploit module""", "green")
   
		return True

	# Load modules into global namespace
	def preloadModules(self):

		# Add module directory
		sys.path.append("modules")

		# Create a list of available modules
		module = glob.glob("modules/*.py")
		
		# Place each module in the global namespace
		for i in range(len(module)):
			
			module[i] = module[i].split(".")[0].split("/")[1]
			module[i] = "modules."+module[i]
			globals()[module[i]] = self.ezImport(module[i])

		return True

	# Verify Module is set
	def verifyModule(self):

		# Verify that there is a currently loaded module
		if self.framework.module == None:

			print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
			print "No module defined"
			return False

		return True

	# Load a module
	def loadModule(self, modname):
		
		# Verify that the module exists
		if not os.path.isfile("modules/"+modname+".py"):
			print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
			print modname + " is not a valid module "
			return False
		
		# Empty framework module property
		self.module = None

		# Generate name of module to load
		mod = "modules."+modname
		
		# Attempt to import and create an instance of module
		try:
			module = self.ezImport(mod)
			self.module = module(self)
		except:
			print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
			print modname + " is not a valid module "
			return False

		# Verify that module loaded correctly
		if self.module == None:
			print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
			print "Error loading module " + module
			return False

		# Merge default variables with module variables
		self.variables = dict(self.defaultVariables.items() + self.module.variables.items())
		print self.prompt+self.libs.colours.cstring(' ~> ', 'white')+self.libs.colours.cstring("Module " + self.module.name + " loaded", "green")

		return True

	# List currently available Modules
	def listModules(self):

		# Ensure all modules are loaded
		self.preloadModules()

		# Generate a list of all available modules
		classes = glob.glob("modules/*.py")

		# Verify each module in the directory exists in the namespace, display name and description of the ones that match
		for i in range(len(classes)):
			classes[i] = classes[i].split(".")[0].split("/")[1]
			if classes[i] == '__init__':
				continue
			classes[i] = "modules."+classes[i]
			if classes[i] in globals():
				try:
					mod = self.ezImport(classes[i])
					module = mod(self)
				except:
					continue
				print self.prompt+self.libs.colours.cstring(' ~> ', 'white')+self.libs.colours.cstring(module.name+" - "+module.description, "blue")
				module = None

		return True

	# Returns the type of module in use
	def listType(self):

		return self.modType

	# Method to dynamically load modules
	def ezImport(self, name):
		components = name.split('.')

		# Obtain module name
		comp = components[1]
		
		# Attempt to import module
		try:
			mod = __import__(name, fromlist=[comp])
			mod = getattr(mod, comp)
		except:
			return False

		return mod

	# Display module variables
	def showVariables(self):
		
		# Verify module is loaded
		if not self.verifyModule():
			return False

		# Check to see if all required variables are set
		self.verifyVariables()

		# Print module variables and information
		for key, variable in self.variables.items():
			required = '*' if variable['required'] else ' '
			
			print self.libs.colours.cstring("\t"+required, "red"),
			print self.libs.colours.cstring(key, "blue"),
			if len(key) < 10:
				print "\t",
			print " => ",
			if hasattr(self.module, key):
				val = getattr(self.module, key)
				print self.libs.colours.cstring(val, "green"),
			else:
				val = "Empty"
				print self.libs.colours.cstring(val, "red"),
			if len(val) < 10:
				print "\t",
			print " => ",
			print self.libs.colours.cstring(variable['description'], "light_purple")

		print self.libs.colours.cstring("\n\t*", "red"),
		print self.libs.colours.cstring(" = required", "green")

	# Determine if a variable name is valid
	def variableExists(self, variable):
		return variable in self.variables

	# Check if required variables are set
	def verifyVariables(self):

		# Check through each variables
		for key, data in self.variables.items():
			
			# Ensure variable property has been set
			check = hasattr(self.module, key)

			# Check if variable is required, and if it has been defined
			if data['required'] == True and not check:
				print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
				print "Missing Required Variable " + key
				return False

			# Check if variable is not required, and if it has been defined
			if data['required'] == False and not check:
				
				setattr(self.module, key, self.variables[key]['default'])

		return True

	# Set module variable value
	def setValue(self, variable, value):

		# Check if module is valid
		if self.verifyModule() == False:
			
			return False

		# Check that variable submitted is a valid module variable
		if self.variableExists(variable) == False:
			print self.prompt+self.libs.colours.cstring(' ~> ', 'white'),
			print "Variable " + variable + " doesn't exist"
			return False

		# Set module variable
		setattr(self.module, variable, value)
		return True


	# Check target for vulnerability
	def checkExploit(self):

		#Check that module and variables are valid
		if self.verifyModule() == False:
			return False
		if self.verifyVariables() == False:
			return False

		# Clear Thread Queue
		self.clearThreads()

		# Run Module Defined check method
		vulnerable = self.module.check()

		if vulnerable:
			print self.printBox("green")+ "The target is vulnerable"
		else:
			print self.printBox("red")+"The target is not vulnerable"

		return True


	# Print current time to terminal
	def printTime(self):

		print self.prompt+self.libs.colours.cstring(' ~> ', 'white')+self.libs.colours.cstring(time.strftime('%l:%M%p %Z'), "green")

	# Run currently loaded exploit
	def runExploit(self):

		# Verify module and variables
		if self.verifyModule() == False:
			return False
		if self.verifyVariables() == False:
			return False

		# Clear thread Queue
		self.clearThreads()

		# Make sure target is vulnerable
		vulnerable = self.module.check()

		if vulnerable == False:
			print " The target is not vulnerable"
			return False
		print self.printBox("green")+" Running exploit..."

		# Run Exploit
		status = self.module.exploit()

		if status == False:
			print self.printBox("red")+" Exploit failed!"
			return False

		print self.printBox("green")+" Exploit Successful!"

		return True

	# Clear the terminal
	def clearScreen(self):
		
		os.system('clear')
		return True

	# Returns the elapsed time of execution
	def getExecutionTime(self, message=False):

		seconds = time.time() - self.framework.time

		if message:

			if seconds < 60:
				seconds = round(seconds, 2)
				message = str(seconds) + " seconds"
			elif seconds < 3600:
				minutes = math.floor((seconds / 60) % 60)
				seconds = math.floor(seconds % 60)
				message = str(minutes) + " minutes and " + str(seconds) + " seconds"
			else:
				hours = math.floor(seconds / 3600)
				minutes = math.floor((seconds / 60) % 60)
				seconds = math.floor(seconds % 60)
				message = str(minutes) + " minutes and " + str(seconds) + " seconds"
		else:
			return seconds

		return message

	# Generates path from URL and directory path
	def getURL(self):

		if self.verifyModule() == False:
			return False
		return self.framework.module.target + self.framework.module.path

	# Obtain output from HTTP Thread
	def getOutput(self, handle):
		# TODO
		return True

	# Get Cookies from HTTP Thread
	def getCookies(self, output):
		# TODO
		return True

	# Add a thread to the Queue
	def addThread(self, options):
		self.framework.threadArray.append(options)
		return True

	# Empty the Thread Queue
	def clearThreads(self):
		
		self.framework.threadArray = []

	# Execute HTTP Threads
	def runThreads(self, callback):

		# Declare IO Queues
		options_q = Queue.Queue
		result_q = Queue.Queue

		# Determine threadcount
		threadCount = len(self.framework.threadArray)
		
		counter = 0
		
		# Populate Input Queue
		while self.framework.currentThread < threadCount and self.framework.currentTrhead < self.maxThreads:
			options_q.put(self.framework.threadArray[counter])
			counter += 1
		
		# Spawn Threads
		print "\t"+self.printBox("blue") + "Spawning " + str(threadCount) + " threads."
		pool = [HTTPThread(options_q=options_q, result_q=result_q) for i in range(threadCount)]

		# Start Threads
		for thread in pool:
			thread.start()

		# Obtain Output Queue
		while counter > 0:
			counter -= 1
			try:
				result = result_q.get()
				callbackf = getattr(self.framework.module, callback)
				callbackf(result)
			except:
				continue

		return True

	# HAL-9000 Easter Egg
	def hal(self, statement=0):

		# Print HAL Portrait
		self.hal_img()

		# Print Hal Speech
		print "\t",
		if statement == 0:
			print self.libs.colours.cstring(" I'm afraid I can't let you do that Dave", "red")

		elif statement == 1:
			print self.libs.colours.cstring(" I'm scared Dave", "red")

		else:
			print """
	Daisy Daisy give me your answer do
	I'm half crazy over the likes of you
	It won't be a stylish marrige
	I can't afford a carriage
	"""

	# HAL Portrait
	def hal_img(self):
		print """
	@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	@@@@@@#:,,....`............,,..`..```````.......`....:@@@@@@
	@@@@@@#,::,,,,,,,,,,,,,,,:::::,,,,,,,,,,,,,,,,,,,,,,.:@@@@@@
	@@@@@@#,@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,:@@@@@@
	@@@@@@#,@@###########@@@@@#####@####@@#############@.:@@@@@@
	@@@@@@#,@@@#@@@@@@@@####@@@@####@##########@#######@.:@@@@@@
	@@@@@@#,#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.:@@@@@@
	@@@@@@#,@@#;;;;;;;;;;;;;;;;;;;+++++++++++++++++++,#@.:@@@@@@
	@@@@@@#.@@@;;;;;;;;;;;;;;;;;;;##@@#@###@@##@#####:@@.:@@@@@@
	@@@@@@#,#@@;;;;;;,';;'; `;:;;;#`#`@ # #:'+.#`####:@@.:@@@@@@
	@@@@@@#,##@;;;;;;,';;;;, ;:';;# ##@+#`;@#` ######:@@.:@@@@@@
	@@@@@@#,##@;;;;;;,';;'.:,::';;#' ;@+#`:@#` ######:@@.:@@@@@@
	@@@@@@#.##@;;;;;;,';;' ;' :';;#.@.@.# +#@;`@;####:@@.:@@@@@@
	@@@@@@#.@@@;;;;;;:';;;;;;,;..:##,@#+,##:,#@,'####:#@.:@@@@@@
	@@@@@@#.##@;;;;;;;;;;;;;;;;;;;############+######:@@.:@@@@@@
	@@@@@@#,#@@,...............,..,::::::::::::::::::`@@.:@@@@@@
	@@@@@@#.@@@@@@@@@@@@@@@@@@@@@@@#@@#@@@#@@@@##@@@#@@@.:@@@@@@
	@@@@@@#,@#@##@@@@##@@@@#@##@########@########@##@#@@.:@@@@@@
	@@@@@@#,##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@.:@@@@@@
	@@@@@@#:###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@,;@@@@@@
	@@@@@@#:##@@@@@@#@@@@@@#@@@@@##@@###@@@@#@@@@@@@@##@,;@@@@@@
	@@@@@@#:###@@@@@@@#@##@@@@@@++++#@@#@#@##@@@@@@@@##@,;@@@@@@
	@@@@@@#:###@@@@@@@@#@##@.          `#@#@@@@@@@@@@##@,;@@@@@@
	@@@@@@#:###@@@@@@@@@@'   `,:;;;;:,`   ;@@#@@#@@@@#@@,;@@@@@@
	@@@@@@#:###@@@@@@@##   ;';;+#@@#+';;;`` '@@@@@@#@#@@,;@@@@@@
	@@@@@@#:###@@@@@@@,.`';'@@@#';'+#@@@+;'`` @##@@@@##@,;@@@@@@
	@@@@@@#:@##@@@@@@ .:'+@@''#@@@@@@#'#@@+;;``@#@@@@##@,;@@@@@@
	@@@@@@#:@##@@@@@`.';@@#@@@@@@@@@@@@@##@@;'`.##@#@##@,'@@@@@@
	@@@@@@#:##@##@@`.''@@@@@@@@#####@@@@@@@#@''`.@@#@##@,'@@@@@@
	@@@@@@#:##@##@..''@@@@@@@+:.`.,:;#@@@@@@+@+'..@####@:'@@@@@@
	@@@@@@#:##@##;,''@+@@@@@#,``.+#@##@@@@+;++@++.,#@##@:'@@@@@@
	@@@@@@#:#@@@@,;'@+@;.;@@+.``'@@@@@@@@@#..:+@'',+@#@@,'@@@@@@
	@@@@@@#:@#@#,,+#'@.` #@@#####@@@@@@@@@@':,;;@':.##@@:'@@@@@@
	@@@@@@#:##@@:''##;`.+@@@@@@@@@@@@@@@@@@+##+@#++,'##@:'@@@@@@
	@@@@@@#:@@@:,'@;@;+#@@@@@@@@@######@@@@:@@@@+@',,#@@,;@@@@@@
	@@@@@@#:##@,;'@@@#@@@###@@@@#######@##,##@@@@#+':##@:'@@@@@@
	@@@@@@#:#@+:+##@@@@@##++:++++''+'''''+';'@@@@#@+:;@@:'@@@@@@
	@@@@@@#:#@;,'@@@@@@#''#@###':`:;'''+##+;'@@@@@@':,#@:'@@@@@@
	@@@@@@#:#@,:'@@@@@@@#@@@#'.';,:;+':+##@##@@@@@@'',@@:'@@@@@@
	@@@@@@#:@@,;'@@@@@@@@@@@++;,','+'.;+#@#@@@@@@@@+':@@:'@@@@@@
	@@@@@@#;#@:'+@@@@@@@@@@#++;'++;''';+###@@@@@@@@#':#@:'@@@@@@
	@@@@@@#:@@:'+@@@@@@@@@@##++'+```'+++##@@@@@@@@@#':#@:'@@@@@@
	@@@@@@#:#@:'+@@@@@@@@@@##+++'. .;+++##@@@@@@@@@#':#@:'@@@@@@
	@@@@@@#:#@:'+@@@@@@@@@@##++++...++++##@@@@@@@@@#':#@:'@@@@@@
	@@@@@@#:@@:;'@@@@@@@@@@##+++++'+++++##@@#@@@@@@+':#@:'@@@@@@
	@@@@@@#:@@::'@@@@@@@@@@###+++++++++###@@@@@@@@@'':@@:'@@@@@@
	@@@@@@#;##;:'@@@@@@@@@@####++++++++##@@@@@@@@@@'::@@:'@@@@@@
	@@@@@@#:##+:'#@@;+@@@@@@####+++++###@@@@@@@@@@@':;@@:'@@@@@@
	@@@@@@#;##@:;'@@':;@@@@@@##########@@@@@@@@@@@'':##@:'@@@@@@
	@@@@@@#;#@#;:'@@#:,.:@@@@@@#######@@@@@@@@@@@@'::@@@:'@@@@@@
	@@@@@@#;@@@#:''@@',,,.,+@@@@@#@@#@@@@@@@@@@@@+':+@#@:'@@@@@@
	@@@@@@#;@@@@::'@@@:,,.,,.@@#@@@@@@@@@@@@@@@@@';:@##@:'@@@@@@
	@@@@@@#;#@##@:;'@@@,,,,,@@+#'@++++@@@@@@@@@@'':##@#@:'@@@@@@
	@@@@@@#;#@##@;;''@@@,,:@@@@@@@@@@@@@+@@@@@@''::@@@@@:'@@@@@@
	@@@@@@#;#@####::+'@@@;@@@@@@@@@@@@@@@@@@@@+'::@@@@@@:'@@@@@@
	@@@@@@#;#@#@##@,:''@@@@@@@@@@@@@@@@@@@@@@'+::@@@@@@@:'@@@@@@
	@@@@@@#;##@@@#@@::''@@@@@@@@@@@@@@@@@@@@''::@@@@@@@@:'@@@@@@
	@@@@@@#;##@@@@#@@,:''+@@@@@@@@@@@@@@@@+''::@#@@@@@@@:'@@@@@@
	@@@@@@#;@@@@@@@@#@;;;'''@@@@@@@@@@@@+'';::@##@@@@@@@:'@@@@@@
	@@@@@@#;@@#@@@@##@@#:;;''''+##@#+'''';::+#@#@@@@@@#@:'@@@@@@
	@@@@@@#;@#@@@@@@@@@@@+:;:;'''''''';:::'@@@#@@@@@@@@@:'@@@@@@
	@@@@@@#;@#@@@@@@@@@@##@@':::;:::;::;#@@#@@@@@@@@@@@@:'@@@@@@
	@@@@@@#;##@@@@@@@@@##@@@#@@@####@@@@@@#@###@@@@@@@@@:'@@@@@@
	@@@@@@#;#@@@@#########@@######@@#@####@####@#@###@@@:'@@@@@@
	@@@@@@#;#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:'@@@@@@
	@@@@@@#'::,,::,,,::,,,:,,,,,,,,,:,,,,,,,,,,,,,,,,,,:;'@@@@@@
	@@@@@@#;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;';;'@@@@@@

"""

	# Print a formatted Box like [*]
	def printBox(self, colour="red", icon="*", border="dark_gray"):
		return self.libs.colours.cstring("[", border)+self.libs.colours.cstring(icon, colour)+self.libs.colours.cstring("] ", border)

	def genList(self):

		files = glob.glob("modules/*.py")
		for word in files:
			if '__init__' in word: continue
			self.autocomp.append(word[8:-3])

		files = glob.glob("libs/*.py")
		for word in files:
			if '__init__' in word: continue
			self.autocomp.append(word[5:-3])

		return True