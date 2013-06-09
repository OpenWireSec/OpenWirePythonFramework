# This file is part of the OpenWire Framework.
#
#    OpenWire is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenWire is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenWIre.  If not, see <http://www.gnu.org/licenses/>.

"""
openWire Python Framework
Design based on 0x0F php Framework
By: Phaedrus
Date: March 2, 2013

A basic exploitation framework, can dynamically load modules and libraries
includes a builtin multithreaded HTTP Handler 
"""

# Import These Modules
from cor import *
from lib import *
import HTTPThread
import subprocess
import completer
import readline
import Queue
import math
import time

# openWire Framework
class Framework:

	def __init__(self):
		self.core = core(self)
		self.libs = libraries(self)
		self.time = time.time()
		self.module = None
		self.prompt = "openWire"
		self.threads = 10
		self.queries = 0
		self.modType = None
		self.modTypes = ['exploit', 'aux', 'payload', 'post']
		self.regexURL = "#^(https?://)?[a-zA-Z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$#"
		self.fw = self
		self.variables = {}
		self.useragent = "Mozilla/5.0 (X11 Linux i686) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/10.04 Chromium/17.0.963.56 Chrome/17.0.963.56 Safari/535.11"
		self.regexPath = "#^[a-zA-Z0-9\.\-_~\!\$&\'\(\)\*\+,\=\:@/]+$#"
		self.threadArray = []
		# Placeholder for Default Variables, uncomment and modify below to set required variables for all modules
		#self.defaultVariables = {'target' : {'required' : True, 'description' : 'The target host (ex. www.google.com)'}}
		self.defaultVariables = {}
		self.autocomp = ['use', 'view', 'load', 'run', 'exploit', 'check', 'show', 'variables', 'set', 'help', 'list', 'libs', 'clear', 'cls', 'banner', 'exit', 'stop', 'quit', 'time', 'target', 'aux', 'payload']
		
		#Aliases for programmer convenience
		self.printBox = getattr(self.core.coreMain, 'printBox')
		self.cstring = getattr(self.libs.colours, 'cstring')
		
	def run(self):
		#preload libraries
		self.core.coreModules.preloadModules()
		self.core.coreMain.outputHeader()
		
		
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
				self.prompt = self.cstring('(', 'red')+self.cstring("openWire", 'light_blue')+self.cstring("->", "red") + self.cstring(self.module.name, "white")+self.cstring(')', 'red')
			else:
				self.prompt = self.cstring('(', 'red')+self.cstring("openWire", 'light_blue')+self.cstring(')', 'red')
			
			# Read user input
			sys.stdout.write(self.prompt)
			sys.stdout.write(' ') 
			line = raw_input()
			
			# Parse user input
			if line == "" or line in exitCommands:
				continue

			self.parseInput(line)

	# Parse user Input
	def parseInput(self, line):

			commands = line.split(" ")

			# Print Help Message
			if commands[0] == 'help':
				self.core.coreMain.showUsage()
			

			# List available Modules
			elif commands[0] == 'list':
				self.core.coreModules.listModules()

			# Unload currently selected module
			elif commands[0] == 'back':
				self.module = None
				
			# Load a module
			elif commands[0] == 'use' or commands[0] == 'load':
			
				if len(commands) < 3:
					self.core.coreMain.showUsage()
					return False
				self.modType = commands[1]
				if commands[1] == "exploit" or commands[1] == "aux" or commands[1] == "payload":
					self.core.coreModules.loadModule(commands[2].lower())
				else:
					self.core.coreMain.showUsage()
			
			# Set current modules variables
			elif commands[0] == 'set':
			
				if len(commands) < 3:
					self.core.coreMain.showUsage()
					return False
				self.core.coreModules.setValue(commands[1], ' '.join(commands[2:]))
			
			elif commands[0] == 'globals':
				for stuff in self.modTypes:
					for items in globals():
						if stuff in items:
							print items

			# show current modules variables
			elif commands[0] == 'show':
			
				if commands[1] == 'variables':
					self.core.coreModules.showVariables()
				else:
					self.core.coreMain.showUsage()

			# show current modules variables
			elif commands[0] == 'view':
				
				self.core.coreModules.showVariables()
			
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
				self.core.coreMain.outputHeader()

			# Disable HAL-9000 Higher Function Modules
			elif commands[0] == 'pewpew':
				self.hal(1)
			elif commands[0] == 'nmap':
				self.nmap(commands)

			# Try to kill HAL-9000 system
			elif commands[0] == 'die':
				self.hal()

			elif commands[0] == 'game':
				self.game()

			elif commands[0] == 'refresh':
				self.update()

			# Handle incorrect input
			else:
				print self.prompt+self.cstring(' ~> ', 'white'), 
				print "%s is not a valid command" % commands[0]



	# Check target for vulnerability
	def checkExploit(self):
		
		#Check that module and variables are valid
		if self.core.coreModules.verifyModule() == False:
			return False
		if self.core.coreModules.verifyVariables() == False:
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

		print self.prompt+self.cstring(' ~> ', 'white')+self.cstring(time.strftime('%l:%M%p %Z'), "green")

	# Run currently loaded exploit
	def runExploit(self):
		
		# Verify module and variables
		if self.core.coreModules.verifyModule() == False:
			return False
		if self.core.coreModules.verifyVariables() == False:
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

		seconds = time.time() - self.fw.time

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
				message = str(hours) + " hours and " +str(minutes) + " minutes and " + str(seconds) + " seconds"
		else:
			return seconds

		return message

	# Generates path from URL and directory path
	def getURL(self):

		if self.core.coreModules.verifyModule() == False:
			return False
		return self.fw.module.target + self.fw.module.path

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
		self.fw.threadArray.append(options)
		return True

	# Empty the Thread Queue
	def clearThreads(self):
		
		self.threadArray = []

	# Execute HTTP Threads
	def runThreads(self, callback):

		# Declare IO Queues
		options_q = Queue.Queue
		result_q = Queue.Queue

		# Determine threadcount
		threadCount = len(self.fw.threadArray)
		
		counter = 0
		
		# Populate Input Queue
		while self.fw.currentThread < threadCount and self.fw.currentTrhead < self.maxThreads:
			options_q.put(self.fw.threadArray[counter])
			counter += 1
		
		# Spawn Threads
		print "\t"+self.printBox("blue") + "Spawning " + str(threadCount) + " threads."
		pool = [HTTPThread.HTTPThread(options_q=options_q, result_q=result_q) for i in range(threadCount)]

		# Start Threads
		for thread in pool:
			thread.start()

		# Obtain Output Queue
		while counter > 0:
			counter -= 1
			try:
				result = result_q.get()
				callbackf = getattr(self.fw.module, callback)
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
			print self.cstring(" I'm afraid I can't let you do that Dave", "red")

		elif statement == 1:
			print self.cstring(" I'm scared Dave", "red")

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

	def nmap(self, params):
		""" basic nmap wrapper, passes
		parameters to nmap via Popen"""
		subprocess.Popen(params)

	def game(self):
		print "Hello Professor Falken, Would you like to play a Game?"

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

	def update(self):
		self.core.coreModules.preloadModules()
		self.libs.preloadLibs()

		return True