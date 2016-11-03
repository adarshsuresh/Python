import sys,os,timeit
from per_learn import perlearn
from avg_per_learn import avgperlearn
from per_classify import perclassify

def calculatePerformance(dev):
    perlearnclassify = perclassify("")
    perlearnclassify.readmodal()
    cspamfiles = 0
    spamfiles = 0
    chamfiles = 0
    hamfiles = 0
    correctlyclassifiedspam = 0
    correctlyclassifiedham = 0
    for root, dirs, files in os.walk(dev):
        perlearnclassify.path = root
        if root.endswith('/spam'):
            spamcount, hamcount, totalfiles = perlearnclassify.classify()
            spamfiles += totalfiles
            cspamfiles += spamcount
            chamfiles += hamcount
            correctlyclassifiedspam += spamcount
        elif root.endswith('/ham'):
            spamcount, hamcount, totalfiles = perlearnclassify.classify()
            hamfiles += totalfiles
            cspamfiles += spamcount
            chamfiles += hamcount
            correctlyclassifiedham += hamcount

    precisionspam = correctlyclassifiedspam / cspamfiles
    recallspam = correctlyclassifiedspam / spamfiles
    f1scorespam = (2 * precisionspam * recallspam) / (precisionspam + recallspam)

    precisionham = correctlyclassifiedham / chamfiles
    recallham = correctlyclassifiedham / hamfiles
    f1scoreham = (2 * precisionham * recallham) / (precisionham + recallham)


    print("HAM:", "Precision:", precisionham, "Recall:", recallham, 2, "F1score:",
          f1scoreham)
    print("SPAM:", "Precision:", precisionspam, "Recall:", recallspam, "F1score:",
          f1scorespam)

def main():
    training = sys.argv[1]
    dev = sys.argv[2]
    learnmodal = perlearn(training)
    learnmodal.generatemodal()
    learnmodal.writemodal()
    print("PERCEPTRON LEARN")
    calculatePerformance(dev)
    learnmodal = avgperlearn(training)
    learnmodal.generatemodal()
    learnmodal.writemodal()
    print("AVERAGE PERCEPTRON LEARN")
    calculatePerformance(dev)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    stop = timeit.default_timer()
    print(stop - start)
