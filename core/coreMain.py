'''
Created on 2013-06-08

@author: phaedrus
'''

class coreMain:
    
    def __init__(self, framework):
        self.fw = framework
        self.name = 'Main'
        self.description = 'Main Framework Functions'
    
        # Print banner
    def outputHeader(self):

        self.fw.clearScreen()
   
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

        print self.fw.libs.colours.cstring("""
    OpenWire 0-day Framework, version 1.0-stable
    List of commands and description of usage""", "light_gray")
   
        print self.fw.libs.colours.cstring("""
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
    
    # Print a formatted Box like [*]
    def printBox(self, colour="red", icon="*", border="dark_gray"):
        return self.fw.cstring("[", border)+self.fw.cstring(icon, colour)+self.fw.cstring("] ", border)