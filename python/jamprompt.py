from cmd import Cmd
from jamconfig import Configuration
from candyman import Candyman
from jamie import Jamie
import spur

class JamPrompt(Cmd):

    commands = [ 'installcandyman', 'installjamie']
    configObj = None
      

    def do_installcandyman(self, args):
        try:
            candyman = Candyman(self.configObj)
            candyman.installcandyman()
        except (RuntimeError, TypeError, NameError) as error:
            print(error.original_traceback)
            pass

    def do_complete_installcandyman(self, text, line, begidx, endidx):
        if not text:
            completions =   self.commands[:]
        elif (text=='installcandyman'):
            completions = ['comma seperated machine list']

    def do_installjamie(self, args):
        try:
            jamie = Jamie(self.configObj)               
            jamie.installjamie()
        except (RuntimeError, TypeError, NameError) as error:
            print(error.original_traceback)
            pass

    def do_stopjamie(self, args):
        try:
            jamie = Jamie(self.configObj)
            jamie.stopjamie()
        except(RuntimeError, TypeError, NameError) as error:
            print(error)
            pass

    def do_stopcandy(self, args):
        try:
            candyman = Candyman(self.configObj)
            candyman.stopcandyman()
        except(RuntimeError, TypeError, NameError) as error:
            print(error)
            pass

    def do_startcandy(self, args):
        try:
            candyman = Candyman(self.configObj)
            candyman.startcandyman()
        except(RuntimeError, TypeError, NameError) as error:
            print(error)
            pass

    def do_complete_startjamie(self, text, line, begidx, endidx):
        if not text:
            completions = self.command[:]
        elif(text=='stopjamie'):
            completions = ['comma separated machine list']
    
    def do_startjamie(self, args):
        try:
            jamie = Jamie(self.configObj)
            jamie.startjamie()
        except(RuntimeError, TypeError, NameError) as error:
            print(error.original_traceback)
            pass
    
    def do_complete_installjamie(self, text, line, begidx, endidx):
        if not text:
            completions =   self.commands[:]
        elif (text=='installjamie'):
            completions = ['comma seperated machine list']

    def do_quit(self, args):
        """Quits the program."""
        print "Quitting."
        raise SystemExit
