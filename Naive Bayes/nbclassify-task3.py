import os,timeit,sys,json
from math import log
class nbclassify(object):
    def __init__(self,path):
        self.path=path
        self.vocab={}
        self.spamtokencount=0
        self.hamtokencount=0
        self.vocabcount=0
        self.Pmsgspam=0
        self.Pmsgham=0
        self.wfile=open('nboutput.txt', 'w')

    def classify(self):
        spamcount=0
        hamcount=0
        totalfiles=0
        for root, dirs, files in os.walk(self.path):
            for curfile in files:
                Pmsgspam=self.Pmsgspam
                Pmsgham=self.Pmsgham
                filepath=os.path.join(root, curfile)
                if curfile.endswith(".txt"):
                    totalfiles+=1
                    with open(filepath, "r", encoding='latin1') as rfile:
                        for data in rfile:
                            contentlist = data.strip().split()
                            for token in contentlist:
                                if token in self.vocab:
                                    Pmsgspam+=log((self.vocab[token][0]+1)/(self.spamtokencount+self.vocabcount))
                                    Pmsgham+=log((self.vocab[token][1]+1)/(self.hamtokencount+self.vocabcount))
                    if(Pmsgham==Pmsgspam):
                        print(filepath)
                    if Pmsgspam > Pmsgham:
                        spamcount+=1
                        self.writetofile('spam',filepath)
                    else:
                        hamcount+=1
                        self.writetofile('ham',filepath)
        return spamcount,hamcount,totalfiles

    def readmodal(self):
        with open('nbmodal.txt') as data_file:
            data = json.load(data_file)
        self.vocab=data['data']
        self.hamfilecount=data['hamfilecount']
        self.spamfilecount=data['spamfilecount']
        self.spamtokencount=data['spamcount']
        self.hamtokencount=data['hamcount']
        self.vocabcount=len(self.vocab)
        self.Pmsgspam=log(self.spamfilecount/(self.spamfilecount+self.hamfilecount))
        self.Pmsgham=log(self.hamfilecount/(self.spamfilecount+self.hamfilecount))

    def writetofile(self,category,path):
        self.wfile.write(category+' '+path+'\n')

    def load_stop_words(self):
        with open('stop_words.txt') as data_file:
            data = json.load(data_file)
        self.stop_words = data['stop_words']

def main():
    mydir = sys.argv[1]
    classify=nbclassify(mydir)
    classify.readmodal()
    classify.classify()
    classify.wfile.close()



if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(stop - start)