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

import httplib2
import threading
import Queue

# HTTPThread handles concurrent HTTP Requests

class HTTPThread(threading.Thread):

	def __init__(self, options_q, reqult_q, proxy=None, timeout=30):
		
		super(HTTPThread, self).__init__()
		
		self.name = self.getName()
		self.options_q = options_q
		self.result_q = result_q
		self.options = options()
		self.timeout = timeout
		self.h = None
		self.proxy = proxy

	def run(self):
		
		while not self.stoprequest.isSet():
			try:
				options = self.options_q.get(True, 0.05)
				for key, val in options:
					setattr(self.options, key, val)
				result = self.requestData()
				self.result_q.put(result)
			except:
				continue

	def join(self, timeout=0.5):
		
		self.stoprequest.set()
		super(HTTPThread, self).join(0.05)

	def requestData(self):

		if hasattr(self.options, 'proxy'):
			proxy = self.proxy.split(":")
			self.h = httplib2.Http(proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, proxy[0], int(proxy[1])), timeout=self.timeout)
		else:
			self.h = httplib2.Http(timeout=self.timeout)

		if not hasattr(self.options, 'url') or not hasattr(self.options, 'method'):
			return False

		
# Dummy class used as container for dynamic variables

class options: pass
