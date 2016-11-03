import os,timeit,sys,json

class perclassify(object):
    def __init__(self, path,output="per_output.txt"):
        self.path = path
        self.outputfile=output
        self.weightdict={}
        self.bias=0
        self.wfile = open(self.outputfile, 'w')

    def classify(self):
        spamcount=0
        hamcount=0
        totalfiles=0
        for root, dirs, files in os.walk(self.path):
            for curfile in files:
                alpha=0
                filepath = os.path.join(root, curfile)
                if curfile.endswith(".txt"):
                    totalfiles+=1
                    with open(filepath, "r", encoding='latin1') as rfile:
                        for data in rfile:
                            contentlist = data.strip().split()
                            for token in contentlist:
                                if token in self.weightdict:
                                    alpha+=self.weightdict[token]
                    if alpha>0:
                        spamcount+=1
                        self.writetofile('spam', filepath)
                    else:
                        hamcount+=1
                        self.writetofile('ham', filepath)
        return spamcount,hamcount,totalfiles

    def readmodal(self):
        with open('per_modal.txt') as data_file:
            data = json.load(data_file)
        self.weightdict=data['weightdict']
        self.bias=data['bias']

    def writetofile(self, category, path):
        self.wfile.write(category + ' ' + path + '\n')

def main():
    mydir = sys.argv[1]
    outputfile=sys.argv[2]
    classify=perclassify(mydir,outputfile)
    classify.readmodal()
    classify.classify()
    classify.wfile.close()

if __name__ == '__main__':
    main()