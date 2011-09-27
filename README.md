Python-Javascript
=================

A pure-python implementation of JavaScript, including both the runtime, parser, tokenizer, etc. etc. etc.

Because you might have thought JS was getting a bit too fast, and wanted to go back to the olden days of mid-90's JS speeds.

Or you might want to run your JS test suite in your Python test suite, like a boss.

Or you just want a coffeescript compiler without having to install node.

Reasons! They're tenuous, but they exist!

This is a WIP
-------------

Things are very, very broken at the moment. Only a few select classes from the JS runtime are implemented -- enough to get things started.

Example
-------

An example script:

````javascript
b = {toString:function(mode) { return mode || 'guy'; }};

if(a < b) {
  return "hey there "+b+' or '+b.toString('gal');
} else if (a > b) {
  return this;
} else return hi;
````

And the example code you'd have to write alongside to run it:

````python
from javascript.runtime import Runtime

with open('test.js', 'r') as f:
    data = f.read()

runtime = Runtime()
print runtime.run(data, {
    'a':1,
    'b':2,
    'c':'Gary Busey'
})
````

Or, if you like exceptionally painful experiences, feel free to run the repl:

````bash
python -c 'from javascript.repl import run_shell; run_shell()
````

License
-------

MIT
