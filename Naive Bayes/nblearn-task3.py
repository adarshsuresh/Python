import os,json,sys,re,string

class nblearn(object):
    def __init__(self, path):
        self.path=path
        self.vocab={}
        self.stop_words=[]
        self.spamtokencount=0
        self.hamtokencount=0
        self.spamfilecount=0
        self.hamfilecount=0

    def generatemodal(self):
        for root, dirs, files in os.walk(self.path):
            if root.endswith('/spam'):
                self.updatedict(root,files,0)
            elif root.endswith('/ham'):
                self.updatedict(root,files,1)

    def updatedict(self,root,files,sh):
        for curfile in files:
            if curfile.endswith(".txt"):
                if sh:
                    self.hamfilecount+=1
                else:
                    self.spamfilecount+=1
                rfile=open(os.path.join(root, curfile), "r", encoding='latin1')
                for data in rfile:
                    contentlist=data.strip().split()
                    for token in contentlist:
                        token=re.sub('[%s]' % re.escape(string.punctuation), '', token)
                        if token not in self.stop_words:
                            if sh:
                                self.hamtokencount+=1
                            else:
                                self.spamtokencount+=1
                            if token in self.vocab:
                                self.vocab[token][sh]+=1
                            else:
                                if sh:
                                    self.vocab[token]=[0,1]
                                else:
                                    self.vocab[token]=[1,0]

    def writemodal(self):
        with open('nbmodal.txt', 'w') as wfile:
            json.dump({'spamfilecount':self.spamfilecount,'spamcount':self.spamtokencount,'hamfilecount':self.hamfilecount,'hamcount':self.hamtokencount,'data':self.vocab}, wfile)

    def load_stop_words(self):
        with open('stop_words.txt') as data_file:
            data = json.load(data_file)
        self.stop_words=data['stop_words']

def main():
    mydir = sys.argv[1]
    learnmodal=nblearn(mydir)
    learnmodal.load_stop_words()
    learnmodal.generatemodal()
    learnmodal.writemodal()

if __name__ == '__main__':
    main()