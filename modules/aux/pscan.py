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

import socket
import subprocess
import time

class pscan:

	def __init__(self, framework):
		
		self.name = "pScan"
		self.description = "A simple port scanner"
		self.fw = framework
		self.variables = {}
		self.variables['target'] = {'required' : True, 'description' : 'Target to probe e.g.: 192.168.1.1'}
		self.variables['portrange'] = {'required' : False, 'description' : 'Ports to scan', 'default' : '0-1000'}

	def loadModule(self):

		return True

	def installModule(self):

		return True

	def check(self):

		print self.fw.printBox("red")+"This module does not support check"

		return True

	def exploit(self):
		self.fw.time = time.time()
		ret = subprocess.call("ping -c 1 %s" % self.target, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
		if ret == 0:
			print self.fw.printBox("green")+"%s: is up, Performing portscan." % self.target
		else:
			print self.fw.printBox("red")+"%s: is not up, cannot scan ports." % self.target
			return False
		self.scan(socket.gethostbyname(self.target))

		print self.fw.printBox("blue")+" Scan finished in: " + self.fw.getExecutionTime(True)
		return True

	def post(self):

		print self.fw.printBox("blue")+"This module does not support Post Exploit"

		return True


	def scan(self, ip):

		print self.fw.printBox("blue")+self.fw.cstring("Open Ports in range: ", "light_blue"),
		print self.fw.cstring(self.portrange, "green")
				
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
			print "\t"+self.fw.printBox("blue", "+", "green")+self.fw.cstring(ip, "yellow")+self.fw.cstring(":", "green")+self.fw.cstring(str(i), "yellow")

			s.close()
		except:
			pass
		
		
