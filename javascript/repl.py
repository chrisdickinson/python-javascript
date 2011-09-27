import sys
import code
from javascript.thread import Thread
from javascript.runtime import Runtime
from javascript.special_objects import Null, Undefined


class REPL(code.InteractiveConsole, object):
    def __init__(self, output=None, runtime=None):
        super(REPL, self).__init__()
        self.runtime = runtime or Runtime()
        self.output = output or sys.stdout

    def interact(self, banner=None):
        try:
            super(REPL, self).interact(banner)
        except ExitREPL:
            pass

    def map_output(self, item, depth=0):
        if depth > 10:
            return '<maxdepth>'

        if item is Undefined:
            return 'undefined'

        if item is Null:
            return 'null'

        try: 
            return {
                'string':lambda a:'"%s"' % a.value,
                'boolean':lambda a:a.value and 'true' or 'false',
                'number':lambda a:str(a.value),
                'function':lambda a:'<function>',
                'object':lambda a:'{%s}' % u',\n\t'.join([
                    '%s: %s' % (key, self.map_output(a.js_box(self.runtime.thread).js_get_property(self.runtime.thread, key), depth+1)) for key in a.js_box(self.runtime.thread).js_enumerate()])
            }[item.typeof](item)
        except KeyError:
            return '<unk>'

    def runsource(self, source, filename='<input>', symbol='single'):
        if source == 'exit':
            raise ExitREPL()

        if not source:
            return False

        try:
            value = self.runtime.run(source)
            self.output.write(self.map_output(value)+'\n')
        except:
            self.showtraceback()
            return False

class ExitREPL(Exception):
    pass

def run_shell():
    console = REPL()
    console.interact('Python-Javascript')

if __name__ == '__main__':
    run_shell()
