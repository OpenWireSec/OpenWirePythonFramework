import socket
import subprocess
import time

class pscan:

	def __init__(self, framework):
		
		self.name = "pScan"
		self.description = "A simple port scanner"
		self.framework = framework
		self.variables = {}
		self.variables['portrange'] = {'required' : False, 'description' : 'Ports to scan', 'default' : '0-1000'}

	def loadModule(self):

		return True

	def installModule(self):

		return True

	def check(self):

		print self.framework.printBox("red")+"This module does not support check"

		return True

	def exploit(self):
		self.framework.time = time.time()
		ret = subprocess.call("ping -c 1 %s" % self.target, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
		if ret == 0:
			print self.framework.printBox("green")+"%s: is up, Performing portscan." % self.target
		else:
			print self.framework.printBox("red")+"%s: is not up, cannot scan ports." % self.target
			return False
		self.scan(socket.gethostbyname(self.target))

		print self.framework.printBox("blue")+" Scan finished in: " + self.framework.getExecutionTime(True)
		return True

	def post(self):

		print self.framework.printBox("blue")+"This module does not support Post Exploit"

		return True


	def scan(self, ip):

		print self.framework.printBox("blue")+self.framework.libs.colours.cstring("Open Ports in range: ", "light_blue"),
		print self.framework.libs.colours.cstring(self.portrange, "green")
				
		if ',' in self.portrange:
			ports = self.portrange.split(",")
			for port in ports:
				self.connect(ip, int(port))
			return True
		elif '-' in self.portrange:
			ports = self.portrange.split("-")
			start = ports[0]
			stop = ports[1]
		else:
			self.connect(ip, int(self.portrange))
			return True

		for i in range(int(start), int(stop)):
			self.connect(ip, i)

		return True

	def connect(self, ip, i):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((ip, i))
			print "\t"+self.framework.printBox("blue", "+")+self.framework.libs.colours.cstring(ip, "yellow")+self.framework.libs.colours.cstring(":", "green")+self.framework.libs.colours.cstring(str(i), "yellow")

			s.close()
		except:
			pass
		
		
