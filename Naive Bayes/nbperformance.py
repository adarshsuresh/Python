from nbclassify import nbclassify
import os
path='Spam or Ham/dev'
mynbclassify = nbclassify("")
mynbclassify.readmodal()
cspamfiles=0
spamfiles=0
chamfiles=0
hamfiles=0
correctlyclassifiedspam=0
correctlyclassifiedham=0
for root, dirs, files in os.walk(path):
    mynbclassify.path = root
    if root.endswith('/spam'):
        spamcount, hamcount,totalfiles = mynbclassify.classify()
        spamfiles += totalfiles
        cspamfiles += spamcount
        chamfiles += hamcount
        correctlyclassifiedspam+=spamcount
    elif root.endswith('/ham'):
        spamcount, hamcount,totalfiles= mynbclassify.classify()
        hamfiles+=totalfiles
        cspamfiles += spamcount
        chamfiles += hamcount
        correctlyclassifiedham+=hamcount



precisionspam=correctlyclassifiedspam/cspamfiles
recallspam=correctlyclassifiedspam/spamfiles
f1scorespam=(2*precisionspam*recallspam)/(precisionspam+recallspam)

precisionham=correctlyclassifiedham/chamfiles
recallham=correctlyclassifiedham/hamfiles
f1scoreham=(2*precisionham*recallham)/(precisionham+recallham)

print("SPAM:","Precision:",round(precisionspam,2),"Recall:",round(recallspam,2),"F1score:",round(f1scorespam,2))
print("HAM:","Precision:",round(precisionham,2),"Recall:",round(recallham,2),"F1score:",round(f1scoreham,2))