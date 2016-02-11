#!/usr/bin/python
#AI agent to play minmax ,alpha beta and greedy algorithms
import sys,copy
import time
tfile=None
nstate=None
st=time.time()

class GameBoardPlay(object):
    def __init__(self, gameboard=None, Player1=None, Player2=None, Player1algo=0, Player2algo=0, Player1cutoff=0,
                 Player2cutoff=0):
        self.Player1 = Player1
        self.Player2 = Player2
        self.Player1algo = Player1algo
        self.Player2algo = Player2algo
        self.Player1cutoff = Player1cutoff
        self.Player1cutoff = Player2cutoff
        self.gameboard = gameboard

    def changeplayer(self):
        old = copy.deepcopy(self)
        self.Player1 = old.Player2
        self.Player2 = old.Player1
        self.Player1algo = old.Player2algo
        self.Player2algo = old.Player1algo
        self.Player1cutoff = old.Player2cutoff
        self.Player2cutoff = old.Player1cutoff
        self.gameboard.changeplayer()
        self.gameboard.myplayer = self.Player1
        self.gameboard.cuttofdepth = self.Player1cutoff


    def printBoard(self):
        global tfile
        for i in xrange(0, self.gameboard.n):
            tfile.write(''.join(self.gameboard.curgameboard[i]))
            if(i!=self.gameboard.n-1 or self.gameboard.findEmptypos()!=0):
                tfile.write("\n")


class GameBoard(object):
    def __init__(self, size=5, task=0, myplayer=None, curplayer=None, nxtplayer=None, cuttofdepth=0, curgameboard=[],
                 valueboard=[]):
        self.n = size
        self.task = task
        self.myplayer = myplayer
        self.curplayer = curplayer
        self.nxtplayer = nxtplayer
        self.cuttofdepth = cuttofdepth
        self.curgameboard = curgameboard
        self.valueboard = valueboard

    def evalScore(self, player):
        curval = 0
        nxtval = 0
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                if (self.curgameboard[i][j] == player):
                    curval += self.valueboard[i][j]
                elif (self.curgameboard[i][j] != "*"):
                    nxtval += self.valueboard[i][j]
        return curval - nxtval

    def checkAdjacent(self, i, j, player):
        up = 0
        down = 0
        left = 0
        right = 0
        if (i == 0 and j == 0):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i][j + 1] == player):
                right = 1
        elif (i == self.n - 1 and j == self.n - 1):
            if (self.curgameboard[i - 1][j] == player):
                up = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        elif (i == 0 and j == self.n - 1):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        elif (i == self.n - 1 and j == 0):
            if (self.curgameboard[i - 1][j] == player):
                up = 1
            if (self.curgameboard[i][j + 1] == player):
                right = 1
        elif (i == 0):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i][j + 1] == player):
                right = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        elif (j == 0):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i][j + 1] == player):
                right = 1
            if (self.curgameboard[i - 1][j] == player):
                up = 1
        elif (i == 4):
            if (self.curgameboard[i][j + 1] == player):
                right = 1
            if (self.curgameboard[i - 1][j] == player):
                up = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        elif (j == 4):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i - 1][j] == player):
                up = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        elif (i > 0 and j > 0 and i < self.n - 1 and j < self.n - 1):
            if (self.curgameboard[i + 1][j] == player):
                down = 1
            if (self.curgameboard[i][j + 1] == player):
                right = 1
            if (self.curgameboard[i - 1][j] == player):
                up = 1
            if (self.curgameboard[i][j - 1] == player):
                left = 1
        return [up, down, left, right]

    def greedybestfirst(self):
        maxunoccupied = 0
        x = -1
        y = -1
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                sumval = 0
                if ((self.curgameboard[i][j] == "*")):
                    if (1 in self.checkAdjacent(i, j, self.curplayer)):
                        val = self.checkAdjacent(i, j, self.nxtplayer)
                        if (val[0] == 1):
                            sumval += self.valueboard[i - 1][j]
                        if (val[1] == 1):
                            sumval += self.valueboard[i + 1][j]
                        if (val[2] == 1):
                            sumval += self.valueboard[i][j - 1]
                        if (val[3] == 1):
                            sumval += self.valueboard[i][j + 1]
                    if (maxunoccupied < self.valueboard[i][j] + (2 * sumval)):
                        maxunoccupied = self.valueboard[i][j] + (2 * sumval)
                        x = i
                        y = j
        self.nextMove(x, y)

    def nextMove(self, i, j):
        if (1 in self.checkAdjacent(i, j, self.curplayer)):
            val = self.checkAdjacent(i, j, self.nxtplayer)
            if (val[0] == 1):
                self.curgameboard[i - 1][j] = self.curplayer
            if (val[1] == 1):
                self.curgameboard[i + 1][j] = self.curplayer
            if (val[2] == 1):
                self.curgameboard[i][j - 1] = self.curplayer
            if (val[3] == 1):
                self.curgameboard[i][j + 1] = self.curplayer
        self.curgameboard[i][j] = self.curplayer

    def printBoard(self):
        global nstate
        for i in xrange(0, self.n):
            nstate.write(''.join(self.curgameboard[i]))
            if (i < self.n - 1):
                nstate.write("\n")

    def findEmptypos(self):
        c = 0
        for i in xrange(0, self.n):
            for j in xrange(0, self.n):
                if ((self.curgameboard[i][j] == "*")):
                    c += 1
        return c

    def changeplayer(self):
        if (self.curplayer == "X"):
            self.curplayer = "O"
            self.nxtplayer = "X"
        else:
            self.curplayer = "X"
            self.nxtplayer = "O"

    def minMax(self):
        max, x, y = maxNode(self, self.cuttofdepth, -1, -1, self.findEmptypos())
        self.nextMove(x, y)

    def minMaxab(self):
        max, x, y = maxNodeab(self, self.cuttofdepth, -1, -1, self.findEmptypos(), -sys.maxint - 1, sys.maxint)
        self.nextMove(x, y)


def getIndex(i, j):
    return chr(j + ord('A')) + str(i + 1)


def printTraverseLog(gameboard, depth, x, y, val, alpha, beta):
        global tfile
        if (gameboard.task == 2):
            if (depth == gameboard.cuttofdepth):
               tfile.write("\nroot" + "," + str(gameboard.cuttofdepth - depth) + ",")
            else:
                tfile.write("\n" + getIndex(x, y) + "," + str(gameboard.cuttofdepth - depth) + ",")
            if (val == sys.maxint):
                tfile.write("Infinity")
            elif (val == -sys.maxint - 1):
                tfile.write("-Infinity")
            else:
                tfile.write(str(val))
        elif (gameboard.task == 3):
            if (depth == gameboard.cuttofdepth):
                tfile.write("\nroot" + "," + str(gameboard.cuttofdepth - depth) + ",")
            else:
                tfile.write("\n" + getIndex(x, y) + "," + str(gameboard.cuttofdepth - depth) + ",")
            if (val == sys.maxint):
                tfile.write("Infinity")
            elif (val == -sys.maxint - 1):
                tfile.write("-Infinity")
            else:
                tfile.write(str(val))
            if (alpha == -sys.maxint - 1):
                tfile.write(",-Infinity")
            else:
                tfile.write("," + str(alpha))
            if (beta == sys.maxint):
                tfile.write(",Infinity")
            else:
                tfile.write("," + str(beta))


def checkInput(argv):
    if (len(argv) != 3 and argv[1] == "-i"):
        print "Error in commandline arguments"


def maxNode(self, depth, x, y, empty):
    if (depth == 0 or empty == 0):
        curval = self.evalScore(self.myplayer)
        printTraverseLog(self, depth, x, y, curval, 0, 0)
        return curval, x, y
    maxval = -sys.maxint - 1
    x1 = -1
    y1 = -1
    printTraverseLog(self, depth, x, y, maxval, 0, 0)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curgameboard[i][j] == "*")):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.changeplayer()
                curval, x2, y2 = minNode(newboard, depth - 1, i, j, empty - 1)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
                printTraverseLog(self, depth, x, y, maxval, 0, 0)
    return maxval, x1, y1


def minNode(self, depth, x, y, empty):
    if (depth == 0 or empty == 0):
        curval = self.evalScore(self.myplayer)
        printTraverseLog(self, depth, x, y, curval, 0, 0)
        return curval, x, y
    minval = sys.maxint
    x1 = -1
    y1 = -1
    printTraverseLog(self, depth, x, y, minval, 0, 0)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curgameboard[i][j] == "*")):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.changeplayer()
                curval, x2, y2 = maxNode(newboard, depth - 1, i, j, empty - 1)
                if (curval < minval):
                    minval = curval
                    x1 = i
                    y1 = j
                printTraverseLog(self, depth, x, y, minval, 0, 0)
    return minval, x1, y1


def maxNodeab(self, depth, x, y, empty, alpha, beta):
    if (depth == 0 or empty == 0):
        curval = self.evalScore(self.myplayer)
        printTraverseLog(self, depth, x, y, curval, alpha, beta)
        return curval, x, y
    maxval = -sys.maxint - 1
    x1 = -1
    y1 = -1
    printTraverseLog(self, depth, x, y, maxval, alpha, beta)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curgameboard[i][j] == "*")):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.changeplayer()
                curval, x2, y2 = minNodeab(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval > maxval):
                    maxval = curval
                    x1 = i
                    y1 = j
                if (maxval >= beta):
                    printTraverseLog(self, depth, x, y, maxval, alpha, beta)
                    return maxval, i, j;
                alpha = max(alpha, maxval)
                printTraverseLog(self, depth, x, y, maxval, alpha, beta)
    return maxval, x1, y1


def minNodeab(self, depth, x, y, empty, alpha, beta):
    if (depth == 0 or empty == 0):
        curval = self.evalScore(self.myplayer)
        printTraverseLog(self, depth, x, y, curval, alpha, beta)
        return curval, x, y
    minval = sys.maxint
    x1 = -1
    y1 = -1
    printTraverseLog(self, depth, x, y, minval, alpha, beta)
    for i in xrange(0, self.n):
        for j in xrange(0, self.n):
            if ((self.curgameboard[i][j] == "*")):
                newboard = copy.deepcopy(self)
                newboard.nextMove(i, j)
                newboard.changeplayer()
                curval, x2, y2 = maxNodeab(newboard, depth - 1, i, j, empty - 1, alpha, beta)
                if (curval < minval):
                    minval = curval
                    x1 = i
                    y1 = j
                if (minval <= alpha):
                    printTraverseLog(self, depth, x, y, minval, alpha, beta)
                    return minval, i, j
                beta = min(minval, beta)
                printTraverseLog(self, depth, x, y, minval, alpha, beta)
    return minval, x1, y1


def readFile(self, game, inputFile):
    i = 0
    with open(inputFile,'rU') as f:
        content = f.readlines()
    for val in content:
        val = val.replace('\n', '')
        if (i == 0):
            i += 1
            self.task = int(val)
            continue
        if (self.task < 4):
            if (i == 1):
                self.curplayer=val
                self.myplayer=val
                if (val == "X"):
                    self.nxtplayer = "O"
                else:
                    self.nxtplayer = "X"
                i += 1
                continue
            if (i == 2):
                self.cuttofdepth = int(val)
                i += 1
                continue
            if (i >= 3 and i <= 7):
                self.valueboard.append(list(int(x) for x in val.split(' ')))
                i += 1
                continue
            if (i >= 8 and i <= 12):
                self.curgameboard.append(list(val))
                i += 1
                continue
        else:
            if (i == 1):
                game.Player1 = val
                i += 1
                continue
            if (i == 2):
                game.Player1algo = int(val)
                i += 1
                continue
            if (i == 3):
                game.Player1cutoff = int(val)
                i += 1
                continue
            if (i == 4):
                game.Player2 = val
                i += 1
                continue
            if (i == 5):
                game.Player2algo = int(val)
                i += 1
                continue
            if (i == 6):
                game.Player2cutoff = int(val)
                i += 1
                continue
            if (i >= 7 and i <= 11):
                self.valueboard.append(list(int(x) for x in val.split(' ')))
                i += 1
                continue
            if (i >= 12 and i <= 17):
                self.curgameboard.append(list(val))
                i += 1
                continue
    if (self.task == 4):
        self.myplayer = game.Player1
        self.curplayer = game.Player1
        self.nxtplayer = game.Player2
        self.cuttofdepth = game.Player1cutoff


def createOutputfile(game_board):
    global tfile,nstate
    if (game_board.task == 1):
        nstate= open("next_state.txt","w")
    elif (game_board.task == 2):
        tfile= open("traverse_log.txt", "w")
        tfile.write("Node,Depth,Value")
        nstate= open("next_state.txt","w")
    elif (game_board.task == 3):
        tfile=  open("traverse_log.txt", "w")
        tfile.write("Node,Depth,Value,Alpha,Beta")
        nstate= open("next_state.txt","w")
    elif (game_board.task == 4):
        tfile=open('trace_state.txt', 'w')

def closefiles(game_board):
    global tfile,nstate
    if (game_board.task == 1):
        nstate.close()
    elif (game_board.task == 2):
        tfile.close()
        nstate.close()
    elif (game_board.task == 3):
        tfile.close()
        nstate.close
    elif (game_board.task == 4):
        tfile.close


def playGame(game_board_play, emptypos):
    if (emptypos == 0):
        return
    if (game_board_play.Player1algo == 1):
        game_board_play.gameboard.greedybestfirst()
        game_board_play.changeplayer()
        game_board_play.printBoard()
    elif (game_board_play.Player1algo == 2):
        game_board_play.gameboard.minMax()
        game_board_play.changeplayer()
        game_board_play.printBoard()
    elif (game_board_play.Player1algo == 3):
        game_board_play.gameboard.minMaxab()
        game_board_play.changeplayer()
        game_board_play.printBoard()
    playGame(game_board_play, emptypos - 1)


def main():
    game_board = GameBoard(5)
    game_board_play = GameBoardPlay(game_board)
    checkInput(sys.argv)
    readFile(game_board, game_board_play, sys.argv[2])
    createOutputfile(game_board)
    if (game_board.task == 1):
        game_board.greedybestfirst()
        game_board.printBoard()
    elif (game_board.task == 2):
        game_board.minMax()
        game_board.printBoard()
    elif (game_board.task == 3):
        game_board.minMaxab()
        game_board.printBoard()
    elif (game_board.task == 4):
        playGame(game_board_play, game_board.findEmptypos())
    closefiles(game_board)

if __name__ == "__main__":
    main()
    print st-time.time()