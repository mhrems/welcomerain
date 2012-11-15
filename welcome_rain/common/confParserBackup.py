import sys as _sys
from pyparsing import *
import re
from xml.etree.ElementTree import XML, fromstring, tostring

_commajoin = ", ".join
_id = id
_len = len
_type = type

class GMondConfParser:
    """a class which parse gmond.conf file"""
    
    def __init__(self):
        self.prepare()
        pass

    def convertNumbers(s,l,toks):
        n = toks[0]
        try:
            return int(n)
        except ValueError, ve:
            print "Fatal Error : convertNumbers , s=",n
            return float(n)
    
    def joinStrings(s,l,toks):
        """Join string split over multiple lines"""
        return ["".join(toks)]
    
    def createNode(s,l,toks):
        print "---createNode : ",toks
        #print s
        #print l
        #print toks

    def handleValue(s,l,toks):
        print ">>>handleValue : ",toks
        #print s
        #print l
        #print toks

    def handleName(s,l,toks):
        print ">>>handleName : ",toks
    
    def prepare(self):
        confString = dblQuotedString.setParseAction( removeQuotes )
        
        confNumber = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) +
                            Optional( '.' + Word(nums) ) +
                            Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )
        confNumber.setParseAction( self.convertNumbers )
        
        # define basic text pattern for NTP server 
        confNumber2 = Word("0123456789")
        confIPAddress = confNumber2 + "." + confNumber2 + "." + confNumber2 + "." + confNumber2
        
        self.confObject = Forward()
        confValue = Forward()

        confName = Word('$'+'.'+'_'+alphas+nums)
        confName.setParseAction(self.handleName)

        confAlpha = Word('$'+'.'+'_'+alphas+nums)
        #confProperty.setParseAction(self.handleName)

        confField = Word('$'+'.'+'_'+alphas+nums)
        
        #jsonMultiString = (jsonString + Optional(OneOrMore(Suppress(LineEnd()) + LineStart() + jsonString)))
        #jsonMultiString.setParseAction(joinStrings)
        
        #ipAddress = Combine(Word(nums) + ('.' + Word(nums))*3)
        
        confElements = delimitedList( confValue )
        confArray = Group(Suppress('[') + Optional(confElements) + Suppress(']') )
        confValue << ( confAlpha | confNumber | confString )
        #confValue.setParseAction( self.handleValue )
        
        
        #memberDef = Group( confField + Suppress("=") + confValue | Group(self.confObject) | confValue)
        memberDef = Group( confField + Suppress("=") + confValue | Group(self.confObject) )
        memberDef.setParseAction( self.createNode )
        
        confMembers = OneOrMore( memberDef )
        
        commandString = Regex(r'\"(?:\\\"|\\\\|[^"])*\"', re.MULTILINE)
        commandString.setParseAction( removeQuotes )
        #confCommand = Group(CaselessKeyword("include") + restOfLine)
        
        #confCommandValue << ( confName | confNumber | confString )
        confCommand = (CaselessKeyword("include") + Optional(Suppress('(') + confString + Suppress(')')))
        
        self.confObject <<  OneOrMore( (confName + Optional(Suppress('{') + Optional(confMembers) + Suppress('}'))) ) 
        #self.confObject <<  OneOrMore( (confName + Optional(Suppress('{') + Optional(confMembers) + Suppress('}'))) | (confName + Optional(Suppress('(') + Optional(confMembers) + Suppress(')'))) ) 
        #jsonObject << Dict(Optional(jsonMembers))
        
        singleLineCommand = (CaselessKeyword("include") + restOfLine)
        self.confObject.ignore( singleLineCommand )

        confComment = cppStyleComment 
        self.confObject.ignore( confComment )

    def parseInclude(self,src):
        pattern = r'^include(.*)$'
        
        includeList = []
        for match in re.finditer(pattern, src, re.M|re.I):
            includeList.append(match.group())
            #print "matchs=" , match.group()

        result = ['include',includeList]
        return result
    
    
    def parse(self,src,withInclude=True):
        
        try:
            results = self.confObject.parseString(src)
            #print "pyparsing " , results.__class__
            #pprint.pprint(results.asXML())
            if not withInclude:
                return results
            
            resultInclude = self.parseInclude(src)
            dictSrc = results.asList()
            dictSrc.append(resultInclude)

            
            return dictSrc
        
        except ParseException, err:
            print err.line
            print " "*(err.column-1) + "^"
            print err
            return
    
    
                

class GmondConfPrinter:
    def __init__(self):
        self.cmd_include="include"
        self.cmd_modules="modules"
        self.cmd_collection_group="collection_group"
        self.cmd_other="other"
        
    def compareString(self,str1,str2):
        if str1.lower()==str2.lower():
            return True
        return False
        
    def isInclude(self,str):
        return self.compareString(self.cmd_include, str)
    
    def isModules(self,str):
        return self.compareString(self.cmd_modules, str)

    def isCollectionGroup(self,str):
        return self.compareString(self.cmd_collection_group, str)
    
    def isSection(self,obj):
        if not (isinstance(obj, list)):
            return True
        return False
    
    def handleSectionOther(self,items):
        for data in items:
            print data
            
    def pprint(self,parsingResult):
        dataType = ""
        for index,item in enumerate(parsingResult):
        #for item in parsingResult:
            print "index="+str(index)+" , item=",item

            if self.isSection(item):
                if self.isModules(item):
                    dataType=self.cmd_modules
                elif self.isInclude(item):
                    dataType=self.cmd_include
                elif self.isCollectionGroup(item):
                    dataType=self.cmd_collection_group
                else:
                    dataType=self.cmd_other
    
class GmondConf:
    """ """
    
    def __init__(self):
        pass

    def dict2obj(self,d):
        if isinstance(d, dict):
            n = {}
            for item in d:
                #print "GmondConf.dict2obj : item=",item
                if isinstance(d[item], dict):
                    n[item] = dict2obj(d[item])
                elif isinstance(d[item], (list, tuple)):
                    n[item] = [dict2obj(elem) for elem in d[item]]
                else:
                    n[item] = d[item]
            return type('obj_from_dict', (object,), n)
        elif isinstance(d, (list, tuple,)):
            l = []
            for item in d:
                l.append(dict2obj(item))
            return l
        else:
            return d

    def dict2obj2(self,d):
        if isinstance(d, list):
            d = [dict2obj(x) for x in d]
        if not isinstance(d, dict):
            return d
        class C(object):
            pass
        o = C()
        for k in d:
            o.__dict__[k] = dict2obj(d[k])
        return o
    
    def obj_dic(self,d):
        top = type('new', (object,), d)
        seqs = tuple, list, set, frozenset
        for i, j in d.items():
            if isinstance(j, dict):
                setattr(top, i, obj_dic(j))
            elif isinstance(j, seqs):
                setattr(top, i, 
                        type(j)(obj_dic(sj) if isinstance(sj, dict) else sj for sj in j))
            else:
                setattr(top, i, j)
        return top

    def setParseObject(self,data):
        #self.objects = fromstring(text)
        self.objects = self.dict2obj(data);


class dict2obj(dict):
    def __init__(self, dict_):
        super(dict2obj, self).__init__(dict_)
        for key in self:
            item = self[key]
            if isinstance(item, list):
                for idx, it in enumerate(item):
                    if isinstance(it, dict):
                        item[idx] = dict2obj(it)
            elif isinstance(item, dict):
                self[key] = dict2obj(item)

    def __getattr__(self, key):
        return self[key]
        

class ConfPrinter:
    def __init__(self, indent=1, width=80, depth=None, stream=None):
        """Handle pretty printing operations onto a stream using a set of
        configured parameters.

        indent
            Number of spaces to indent for each level of nesting.

        width
            Attempted maximum number of columns in the output.

        depth
            The maximum depth to print out nested structures.

        stream
            The desired output stream.  If omitted (or false), the standard
            output stream available at construction will be used.

        """
        indent = int(indent)
        width = int(width)
        assert indent >= 0, "indent must be >= 0"
        assert depth is None or depth > 0, "depth must be > 0"
        assert width, "width must be != 0"
        self._depth = depth
        self._indent_per_level = indent
        self._width = width
        if stream is not None:
            self._stream = stream
        else:
            self._stream = _sys.stdout

    def setStartChar(self,char):
        self.startChar = char
        
    def setEndChar(self,char):
        self.endChar = char
    
    def setAssignChar(self,char):
        self.assignChar = char
            
    def pprint(self, object):
        self._format(object, self._stream, 0, 0, {}, 0)
        self._stream.write("\n")

    def pformat(self, object):
        sio = _StringIO()
        self._format(object, sio, 0, 0, {}, 0)
        return sio.getvalue()

    def isrecursive(self, object):
        return self.format(object, {}, 0, 0)[2]

    def isreadable(self, object):
        s, readable, recursive = self.format(object, {}, 0, 0)
        return readable and not recursive

    def _conf_safe_repr(self,object, context, maxlevels, level):
        typ = _type(object)
        if typ is str:
            if 'locale' not in _sys.modules:
                return repr(object), True, False
            if "'" in object and '"' not in object:
                closure = '"'
                quotes = {'"': '\\"'}
            else:
                closure = "'"
                quotes = {"'": "\\'"}
            qget = quotes.get
            sio = _StringIO()
            write = sio.write
            for char in object:
                if char.isalpha():
                    write(char)
                else:
                    write(qget(char, repr(char)[1:-1]))
            return ("%s%s%s" % (closure, sio.getvalue(), closure)), True, False
    
        r = getattr(typ, "__repr__", None)
        if issubclass(typ, dict) and r is dict.__repr__:
            if not object:
                return "{}", True, False
            objid = _id(object)
            if maxlevels and level >= maxlevels:
                return "{...}", False, objid in context
            if objid in context:
                return _recursion(object), False, True
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            saferepr = _conf_safe_repr
            for k, v in _sorted(object.items()):
                krepr, kreadable, krecur = saferepr(k, context, maxlevels, level)
                vrepr, vreadable, vrecur = saferepr(v, context, maxlevels, level)
                append("%s: %s" % (krepr, vrepr))
                readable = readable and kreadable and vreadable
                if krecur or vrecur:
                    recursive = True
            del context[objid]
            return "{%s}" % _commajoin(components), readable, recursive
    
        if (issubclass(typ, list) and r is list.__repr__) or \
           (issubclass(typ, tuple) and r is tuple.__repr__):
            if issubclass(typ, list):
                if not object:
                    return "[]", True, False
                format = "[%s]"
            elif _len(object) == 1:
                format = "(%s,)"
            else:
                if not object:
                    return "()", True, False
                format = "(%s)"
            objid = _id(object)
            if maxlevels and level >= maxlevels:
                return format % "...", False, objid in context
            if objid in context:
                return _recursion(object), False, True
            context[objid] = 1
            readable = True
            recursive = False
            components = []
            append = components.append
            level += 1
            for o in object:
                orepr, oreadable, orecur = self._conf_safe_repr(o, context, maxlevels, level)
                append(orepr)
                if not oreadable:
                    readable = False
                if orecur:
                    recursive = True
            del context[objid]
            return format % _commajoin(components), readable, recursive
    
        rep = repr(object)
        return rep, (rep and not rep.startswith('<')), False

    def _format(self, object, stream, indent, allowance, context, level):
        level = level + 1
        objid = _id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        
        rep = self._repr(object, context, level - 1)
        typ = _type(object)
        sepLines = _len(rep) > (self._width - 1 - indent - allowance)
        write = stream.write

        if self._depth and level > self._depth:
            write(rep)
            return

        r = getattr(typ, "__repr__", None)
   
        if ((issubclass(typ, list) and r is list.__repr__) or
            (issubclass(typ, tuple) and r is tuple.__repr__)
           ):
            length = _len(object)
            
            if issubclass(typ, list):
                write(self.startChar)
                endchar = self.endChar
            else:
                write('(')
                endchar = ')'
                
            if self._indent_per_level > 1 and sepLines:
                write((self._indent_per_level - 1) * ' ')
                
            if length:
                context[objid] = 1
                indent = indent + self._indent_per_level
                #print when first elements
                self._format(object[0], stream, indent, allowance + 1,context, level)
                
                level2 = level
                #print when it has second element
                if length > 1:
                    #print "---object---"
                    #print object[1:]
                    #print "finish----"
                    for ent in object[1:]:
                        #print "\n---"
                        #print ent
                        #print "---"
                        objLength = len(ent)
                        #print "level="+str(level)+" , level2="+str(level2)
                        if sepLines:
                            if not isinstance(ent,list):
                                write(' {\n' + ' '*indent)
                            else:
                                write(' ,\n' + ' '*indent)
                                
                            #write(" > level="+str(level)+",length="+str(objLength)+',\n'+' '*indent)
                            #write(',\n' + ' '*indent)
                        else:
                            write(self.assignChar)
                            #write(">>> level="+str(level)+",length="+str(objLength)+"    "+self.assignChar)
                        
                        self._format(ent, stream, indent, allowance + 1, context, level)
                        
                indent = indent - self._indent_per_level
                del context[objid]
            
            if issubclass(typ, tuple) and length == 1:
                write(',')
                
            write(endchar)
            return

        write(rep)

    def _dict(self, object, dict, indent, allowance, context, level):
        level = level + 1
        objid = _id(object)
        if objid in context:
            stream.write(_recursion(object))
            self._recursive = True
            self._readable = False
            return
        
        rep = self._repr(object, context, level - 1)
        typ = _type(object)
        sepLines = _len(rep) > (self._width - 1 - indent - allowance)
        write = stream.write

        if self._depth and level > self._depth:
            write(rep)
            return

        r = getattr(typ, "__repr__", None)
   
        if ((issubclass(typ, list) and r is list.__repr__) or
            (issubclass(typ, tuple) and r is tuple.__repr__)
           ):
            length = _len(object)
            
            if issubclass(typ, list):
                write(self.startChar)
                endchar = self.endChar
            else:
                write('(')
                endchar = ')'
                
            if self._indent_per_level > 1 and sepLines:
                write((self._indent_per_level - 1) * ' ')
                
            if length:
                context[objid] = 1
                indent = indent + self._indent_per_level
                #print when first elements
                self._format(object[0], stream, indent, allowance + 1,context, level)
                
                level2 = level
                #print when it has second element
                if length > 1:
                    #print "---object---"
                    #print object[1:]
                    #print "finish----"
                    for ent in object[1:]:
                        #print "\n---"
                        #print ent
                        #print "---"
                        objLength = len(ent)
                        #print "level="+str(level)+" , level2="+str(level2)
                        if sepLines:
                            if not isinstance(ent,list):
                                write(' {\n' + ' '*indent)
                            else:
                                write(' ,\n' + ' '*indent)
                                
                            #write(" > level="+str(level)+",length="+str(objLength)+',\n'+' '*indent)
                            #write(',\n' + ' '*indent)
                        else:
                            write(self.assignChar)
                            #write(">>> level="+str(level)+",length="+str(objLength)+"    "+self.assignChar)
                        
                        self._format(ent, stream, indent, allowance + 1, context, level)
                        
                indent = indent - self._indent_per_level
                del context[objid]
            
            if issubclass(typ, tuple) and length == 1:
                write(',')
                
            write(endchar)
            return

        write(rep)

    def _repr(self, object, context, level):
        repr, readable, recursive = self.format(object, context.copy(),
                                                self._depth, level)
        if not readable:
            self._readable = False
        if recursive:
            self._recursive = True
        return repr

    def format(self, object, context, maxlevels, level):
        """Format object for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the object represents a recursive construct.
        """
        return self._conf_safe_repr(object, context, maxlevels, level)


        
def readFile(filename):
    f = file(filename)
    s = f.read()
    return s

    
def todict(obj, classkey=None):
    if isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = todict(obj[k], classkey)
        return obj
    elif hasattr(obj, "__iter__"):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.iteritems() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj        


def tuple2dict(data):
    d = {}
    for item in data:
        if len(item) == 1 and isinstance(item, list):
            # remove the nested structure, you may need a loop here
            item = item[0]
            key = item[0]
            value = item[1]
            d[key] = value
            continue
        key = item[0]
        value = item[1]
        if hasattr(value, '__getitem__'):
            value = tuple2dict(value)
        d[key] = value
    return d

def tuple2dict2(_obj):
    _dict = {}
    for item in _obj:
        if isinstance(item, tuple) or isinstance(item, list):
            if isinstance(item[0], basestring):
                _dict[item[0]] = tuple2dict2(item[1])
            else:
                if isinstance(item[0], list):
                    # if the key already exists, then concatenate the old
                    # value with the new one, adding a space in between.
                    _key = item[0][0]
                    if _key in _dict:
                        dict[_key] = item[0][1]
                        #dict[_key] = " ".join([_dict[_key], item[0][1]])
                    else:
                        _dict[_key] = item[0][1]
    return _dict

def t2d(t):
    if isinstance(t,basestring):return t
    length = len(t)
    if length == 1:
        return t2d(t[0])
    if length == 2:
        t1,t2 = t2d(t[0]),t2d(t[1])
        print "T:",t1,t2
        if isinstance(t1,dict) and len(t1) == 1:
            t2['name'] = t1.values()[0]
            t1 = t1.keys()[0]
            return dict([[t1,t2]])
    if length == 3 and isinstance(t[2],bool):
        return t2d(t[:2])

    L1 =[t2d(tp) for tp in t]
    L2 = [lx.items() for lx in L1]
    L3 = dict( [i[0] for i in L2])
    return L3
 
def listToDict(l):
    if type(l) != type([]): return l
    return {l[0] : listToDict(l[1])}

def mergedicts(*dicts):
    """Recursively merge an arbitrary number of dictionaries.
    >>> import pprint
    >>> d1 = {'a': {'b': {'x': '1',
    ...                   'y': '2'}}}
    >>> d2 = {'a': {'c': {'gg': {'m': '3'},
    ...                   'xx': '4'}}}
    >>> pprint.pprint(mergedicts(d1, d2), width=2)
    {'a': {'b': {'x': '1',
                 'y': '2'},
           'c': {'gg': {'m': '3'},
                 'xx': '4'}}}
    """

    keys = set(k for d in dicts for k in d)

    def vals(key):
        """Returns all values for `key` in all `dicts`."""
        withkey = (d for d in dicts if d.has_key(key))
        return [d[key] for d in withkey]

    def recurse(*values):
        """Recurse if the values are dictionaries."""
        if isinstance(values[0], dict):
            return mergedicts(*values)
        if len(values) == 1:
            return values[0]
        raise TypeError("Multiple non-dictionary values for a key.")

    return dict((key, recurse(*vals(key))) for key in keys)

def nested_string_freq(lst):
    ## llst is a nested list of strings
    ## dt is a dictionary 
    def nsf_aux(llst, dt):
        if llst == []:
            return
        else:
            ## split the list llst into
            ## head and tail. 
            head = llst[0]
            tail = llst[1:]
            ## if head is a list, recurse into it
            ## and then recurse into the tail
            if isinstance(head, list):
                nsf_aux(head, dt)
                nsf_aux(tail, dt)
            else:
                ## 1. update the dictionary of string
                ## frequencies
                dt[head] = tail #dt.get(head, 0) + 1
                ## 2. recurse into its tail  
                nsf_aux(tail, dt)
                
    ## define the dictionary 
    dt = {}
    ## call nsf_aux on the input list and dictionary. 
    nsf_aux(lst, dt)
    ## return the dictionary 
    return dt



if __name__ == "__main__":
    
    testdata = """
        /* This collection group will collect the CPU status info every 20 secs.
        The time threshold is set to 90 seconds.  In honesty, this time_threshold could be
        set significantly higher to reduce unneccessary network chatter. */
        include adfafafsafsdf
        glossary {
            collect_every = 20
            time_threshold = 90
            module {
                name = "core_metrics"
            }
            /* Should this be here? Swap can be added/removed between reboots. */            
        }
    """

    import pprint
    
    def printList(src):
        for item in results:
            if not isinstance(item, (tuple, list, dict, set)):
                print "property=",item
            else:
                print "value=",item
 
    def getDepth(l):
        depths = []
        for item in l:
            if isinstance(item, list):
                depths.append(getDepth(item))
        if len(depths) > 0:
            return 1 + max(depths)
        return 1
        
    def printList(items,level,stack):
        def isDataElement(data):
            aItem = data[0]
            if not isinstance(aItem,list):
                if len(data)==2:
                    return True
            return False
        
        def isListDataElement(data):
            aItem = data[0]
            if isinstance(aItem,list):
                if len(data)==1:
                    return True
            return False
        
        def isExist(listData,str):
            for item in listData:
                if item==str:
                    return True
            return False;
        
        indent = 4 
        for index,item in enumerate(items):
            if isinstance(item,list):
                level=level+1
                if isDataElement(item):
                    #print "--- data_element : level="+str(level),item, item[0]+"=",item[1]
                    print " "*level*indent,stack,item[0]+"=",item[1], " level="+str(level)
                    #print " stack = ",stack
                    #stack = []

                elif isListDataElement(item):
                    #print "$$$ listdata_element : level="+str(level),item
                    printList(item,level-1,stack)   
                    #stack.pop()

                else:
                    #print ">>> length="+str(len(item))+",level="+str(level)+",index="+str(index),item
                    #print " "*level*indent,item
                    #stack.append(item)
                    printList(item,level,stack)
                    
                level=level-1
                
                #stack.pop()
                
            else:
                #level=level+1
                #print "length="+str(len(item))+",index="+str(index),item
                if not isinstance(item,list):
                    if level==0:
                        stack = []
                   
                    #if not level==1:
                    if not isExist(stack,item):
                        stack.append(item)
                    
                    print " "*level*indent,item," level="+str(level)
                    #level=level-1

 
                #print "*** level="+str(level)+",index="+str(index),item
                #level=level-1
        
    try:
        
        fileName = "/home/james/Workspace/Project/WelcomeRain/gmond.conf"
        data = readFile(fileName)

        parser = GMondConfParser()
        results = parser.parse(data,True);
        #dictResult = tuple2dict2(results)
        print "class type=",results.__class__
        
        """
        level = 0
        for index,item in enumerate(results):
            if isinstance(item,list):
                level=level+1
            else:
                level=level-1
            print "level="+str(level)+",index="+str(index),item
        """
        
        stackData = []
        printList(results,0,stackData)
        print "----------------"
        print stackData
        
        #pprint.pprint(results)
        #print "class type=",results.__class__
        #print results.dump()
        
        printer = GmondConfPrinter()
        #printer.pprint(results)
        
        
        printer = ConfPrinter(indent=4)
        printer.setStartChar("(")
        printer.setEndChar(")")
        printer.setAssignChar("=")
        #printer.pprint(results)

        """
        for item in results:
            if not isinstance(item, (tuple, list, dict, set)):
                print "property=",item
            else:
                print "value=",item
        """
             
        fmt="%i: %s"
        #for d in enumerate(results):
        #    print(fmt%d)
        #print data
        
        pattern = r'^include(.*)$'
        str = "include ('this is all')\r\n"
        str = str + "include('this')\r\n"
        str = str + "safdsfsdfdsf\r\n"
        str = str + "include ('this is all2')\r\n"
        
        #print str
        
        #for match in re.finditer(pattern, str, re.M|re.I):
        #    print "matchs=" , match.group()
        
        #print re.findall(pattern,str)
   
        #results = jsonObject.parseString(data)
        #print results.asXML()
        #rconf = GmondConf()
        #conf.setParseObject(results.asDict())
                
        #obj = dict2obj(results.asDict())        
        #print results.asList()
        
        #pprint.pprint( results,indent=4 )
        
    except ParseException, err:
        print err.line
        print " "*(err.column-1) + "^"
        print err

    print
    
    def testPrint(x):
        print type(x),repr(x)
    
#    print results[0]
#    print results[1]
#    print results[2]
#    print results[3]
    
#    print
    
#    print results[1][0]
#    print results[1][1]
    
#    print
    
#    print type(results)
    
    #testPrint( results.glossary.collect_every)
#    testPrint( results.glossary.GlossDiv.GlossList.ID )
#    testPrint( results.glossary.GlossDiv.GlossList.FalseValue )
#    testPrint( results.glossary.GlossDiv.GlossList.Acronym )
#    testPrint( results.glossary.GlossDiv.GlossList.EvenPrimesGreaterThan2 )
#    testPrint( results.glossary.GlossDiv.GlossList.PrimesLessThan10 )
