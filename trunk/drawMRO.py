#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, itertools

PSVIEWER = 'gv'     # you may change these with
PNGVIEWER = 'kview' # your preferred viewers
PSFONT = 'Times'    # you may change these too
PNGFONT = 'Courier' # on my system PNGFONT=Times does not work

def if_(cond, e1, e2=''):
    "Ternary operator would be"
    if cond:
        return e1
    else:
        return e2

def MRO(cls):
    """Returns the MRO of cls as a text"""
    out = [ "MRO of %s:" % cls.__name__ ]
    for counter, c in enumerate(cls.__mro__):
        bases = ','.join(b.__name__ for b in c.__bases__)
        s = "    %s - %s(%s)" % (counter, c.__name__, bases)
        if type(c) is not type:
            s += "[%s]" % type(c).__name__
        out.append(s)
    return '\n'.join(out)

class MROgraph(object):
    """Generates the MRO graph of a set of given classes"""
    def __init__(self, *classes, **options):
        if not classes:
            raise "Missing class argument!"
        filename = options.get('filename', "MRO_of_%s.ps" % classes[0].__name__)
        self.labels = options.get('labels', 2)
        caption = options.get('caption', False)
        setup = options.get('setup', '')
        name, dotformat = os.path.splitext(filename)
        viewer = PSVIEWER if dotformat == '.ps' else PNGVIEWER
        self.textrepr = '\n'.join(MRO(cls) for cls in classes)
        if not caption:
            caption = 'caption [shape=box,label="%s\n",fontsize=9];' % self.textrepr
        caption.replace('\n','\\l')
        setupcode = caption + '\n' + setup + '\n'
        codeiter = itertools.chain(*[self.genMROcode(cls) for cls in classes])
        self.dotcode = 'digraph %s{\n%s%s}' % (name, setupcode,
                '\n'.join(codeiter))
        os.system("echo '%s' | dot -T%s > %s; %s %s&" % (self.dotcode, format,
                filename, viewer, filename))

    def genMROcode(self,cls):
        "Generates the dot code for the MRO of a given class"
        for mroindex,c in enumerate(cls.__mro__):
            name=c.__name__
            manyparents=len(c.__bases__) > 1
            if c.__bases__:
                yield ''.join([
                    ' edge [style=solid]; %s -> %s %s;\n' % (
                    b.__name__,name,if_(manyparents and self.labels==2,
                                        '[label="%s"]' % (i+1)))
                    for i,b in enumerate(c.__bases__)])
            if manyparents:
                yield " {rank=same; %s}\n" % ''.join([
                    '"%s"; ' % b.__name__ for b in c.__bases__])
            number=if_(self.labels,"%s-" % mroindex)
            label='label="%s"' % (number+name)
            option=if_(issubclass(cls,type), # if cls is a metaclass
                       '[%s]' % label,
                       '[shape=box,%s]' % label)
            yield(' %s %s;\n' % (name,option))
            if type(c) is not type: # c has a custom metaclass
                metaname=type(c).__name__
                yield ' edge [style=dashed]; %s -> %s;' % (metaname,name)

    def __repr__(self):
        "Returns the Dot representation of the graph"
        return self.dotcode

    def __str__(self):
        "Returns a text representation of the MRO"
        return self.textrepr

def testHierarchy(**options):
    class M(type): pass # metaclass
    class F(object): pass
    class E(object): pass
    class D(object): pass
    class G(object): __metaclass__=M
    class C(F,D,G): pass
    class B(E,D): pass
    class A(B,C): pass
    return MROgraph(A, M, **options)

if __name__=="__main__":
    testHierarchy() # generates a postscript diagram of A and M hierarchies
