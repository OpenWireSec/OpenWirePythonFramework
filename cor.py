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

import sys
import glob
import os

class core:

    def __init__(self, framework):

        self.fw = framework
        self._corelist = self.preloadCore()
        for core in self._corelist:
            if '__init__' in core or '.pyc' in core:
                continue

    # Create an instance of the library
    def loadCore(self, core):

        if core == "core." or "__init__" in core or ".pyc" in core:
            return False
        coref = "core."+str(core)
        if not os.path.isfile("core/"+core+".py"):
            print self.fw.prompt + " " + coref + " is not a valid library"
            return False
        coreFile = self.ezImport(coref)
        setattr(self, str(core), coreFile(self.fw))

    # Import Library
    def ezImport(self, name):
        components = name.split('.')
        comp = components[1]
        mod = __import__(name, fromlist=[comp])
        mod = getattr(mod, comp)
        return mod

    # Load modules into global namespace
    def preloadCore(self):

        sys.path.append("core")
        core = glob.glob("core/*.py")
        core_files = []
        for i in range(len(core)):
            self.loadCore(core[i][5:-3])
            core[i] = core[i].split(".")[0].split("/")[1]
            core[i] = "core."+core[i]
            globals()[core[i]] = self.ezImport(core[i])
            core_files.append(core[i])

        return core_files

    # List installed libraries
    def listCore(self):

        classes = glob.glob("core/*.py")
        for i in range(len(classes)):
            classes[i] = classes[i].split(".")[0].split("/")[1]
            if classes[i] == '__init__':
                continue
            classes[i] = "core."+classes[i]
            if classes[i] in globals():
                core = self.ezImport(classes[i])
                coreFile = core(self)
                #print self.fw.prompt+self.fw.libs.colours.cstring(' ~> ', 'white')+self.fw.libs.colours.cstring(coreFile.name+" - "+coreFile.description, "blue")
                coreFile = None

        return True