import os,re,sys,shutil
from random import randrange
from shutil import copyfile

def main(oldroot,newroot):
    if (not os.path.exists(oldroot)):
        return
    if(os.path.exists(newroot)):
        shutil.rmtree(newroot)
    for root, dirs, files in os.walk(oldroot):
        substr = re.sub(oldroot, '', root)
        curroot = newroot + substr
        os.mkdir(curroot)
        if files:
            nofiles = int(len(files) / 10)
            while nofiles != 0:
                randomnum = randrange(0, len(files))
                copyfile(root + '/' + files[randomnum], curroot + '/' + files[randomnum])
                files.pop(randomnum)
                nofiles -= 1

if __name__ == '__main__':
    oldroot=sys.argv[1]
    newroot=sys.argv[2]
    main(oldroot,newroot)