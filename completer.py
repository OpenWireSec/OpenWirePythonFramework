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
#
# Completer handles the auto-completion features for OpenWire

import readline
import logging


class completer(object):
    
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]                
            else:
                self.matches = self.options[:]
                
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response