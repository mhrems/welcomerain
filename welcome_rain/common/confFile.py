
class ConfFile():
    def __init__(self):
        self.targetPath = ''
        pass
    
    def setPath(self,path):
        self.targetPath = path
        
    def readConf(self):
        conf = []
        file = self.read()
        for line in file:
            #print 1
            #print len(line)
            #print line.isspace()
            #print line
            #conf.append(line.strip())
            # http://creaplz.tistory.com/26
            if not line.isspace():
                #print line
                #print line.replace('\n','').replace('\t','').strip()
                #print len(line)sss
                #print(line)
                #print repr(line)
                edit_line = line.strip()
                conf.append(edit_line)
        
        #print conf
        
        #conf = ['12312']
        return conf
    
    def read(self):
        return open(self.targetPath,"r")
    
    def write(self,data):
        file = open(self.targetPath,"w")
        file.write(data)
        