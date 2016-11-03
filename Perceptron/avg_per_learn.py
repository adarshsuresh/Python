import os,json,sys,random,timeit
from collections import defaultdict


class avgperlearn(object):
    def __init__(self, path):
        self.path = path
        self.weightdict=defaultdict(int)
        self.avgweightdict=defaultdict(int)
        self.bias=0
        self.avgbias=0
        self.counter=1
        self.filevaluedict = {}
        self.filetypedict={}

    def generatemodal(self):
        for root, dirs, files in os.walk(self.path):
            if root.endswith('/spam'):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if filepath.endswith(".txt"):
                        self.filetypedict[filepath] = 1
                        with open(filepath, 'r', encoding='latin1') as content_file:
                            content = content_file.read()
                        tokenlist = content.strip().split()
                        tokendict = defaultdict(int)
                        for token in tokenlist:
                            tokendict[token] += 1
                        self.filevaluedict[filepath] = tokendict
            elif root.endswith('/ham'):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    if filepath.endswith(".txt"):
                        self.filetypedict[os.path.join(root, filename)] = -1
                        with open(filepath, 'r', encoding='latin1') as content_file:
                            content = content_file.read()
                        tokenlist = content.strip().split()
                        tokendict = defaultdict(int)
                        for token in tokenlist:
                            tokendict[token] += 1
                        self.filevaluedict[filepath] = tokendict
        for i in range(0,30):
            self.updateweight()
        for val in self.avgweightdict:
            self.avgweightdict[val]=self.weightdict[val]-(1/self.counter)*self.avgweightdict[val]
        self.avgbias=self.bias-(1/self.counter)*self.avgbias

    def updateweight(self):
        files=list(self.filetypedict.keys())
        random.shuffle(files)
        for curfile in files:
            y = self.filetypedict[curfile]
            contentlist = self.filevaluedict[curfile]
            alpha = 0
            tokenlist = []
            for token in contentlist:
                tokenlist.append(token)
                alpha += self.weightdict[token]*contentlist[token]
            alpha += self.bias
            if y*alpha <= 0:
                for val in tokenlist:
                    self.weightdict[val]+=y*contentlist[token]
                    self.avgweightdict[val]+=y*self.counter*contentlist[token]
                self.bias+=y
                self.avgbias+=y*self.counter
            self.counter+=1

    def writemodal(self):
        with open('per_modal.txt', 'w') as wfile:
            json.dump({'bias': self.avgbias, 'weightdict': self.avgweightdict},wfile)


def main():
    mydir = sys.argv[1]
    learnmodal=avgperlearn(mydir)
    learnmodal.generatemodal()
    learnmodal.writemodal()

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(stop - start)

