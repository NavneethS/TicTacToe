import copy
import random

#Size of the board sz x sz - configurable
sz = 4
board = [['' for i in range(sz)] for i in range(sz)]

nodesgenerated = 0
prunedmax = 0
prunedmin = 0
cutoff = False
maxdepth = 0

#AI player for level-1 difficulty - random move selection
def randompick(state):
    choices = []
    for i in range(sz):
        for j in range(sz):
            if state[i][j]=='':
                choices.append((i,j))

    a = random.choice(choices)
    state[a[0]][a[1]] = 'O'
    return state

#Check for a draw
def isdraw(state):
    #Every square must be filled
    for i in range(sz):
        for j in range(sz):
            if state[i][j]=='':
                return False
    return True

#Pretty print the board
def printboard(state):
    print '--------'*sz
    for i in range(sz):
        for j in range(sz):
            print '|  ', state[i][j], '\t',
        print '|'
        print '--------'*sz

#Return Xn's, On's - rows with n X's and n O's
def rowcheck(state,xs,os):
    #Check for n X/O's in each row for all n from sz to 1
    for r in range(sz):
        row = ''.join(state[r])
        for i in range(sz,0,-1):
            if 'X'*i in row:
                xs[i] += 1
                break
        for i in range(sz,0,-1):
            if 'O'*i in row:
                os[i] += 1
                break
    return xs,os

#Rows,cols,diags with n X/O's
def evalf(state):
    xs = [0]*(sz+1)
    os = [0]*(sz+1)
    xs,os = rowcheck(state,xs,os)
    xs,os = rowcheck(map(list, zip(*state)),xs,os)
    
    d1 = ''.join([state[i][i] for i in range(sz)])
    d2 = ''.join([state[sz-1-i][i] for i in range(sz-1,-1,-1)])

    for d in [d1,d2]:
        for i in range(sz,0,-1):
            if 'X'*i in d:
                xs[i] += 1
                break
        for i in range(sz,0,-1):
            if 'O'*i in d:
                os[i] += 1
                break

    return xs,os

#Given evaluation function
def evalvalue(xs,os):
    return  (6*(xs[3]-os[3]) + 3*(xs[2]-os[2]) + (xs[1]-os[1]))

#Successors of a given state on applying action c
def successors(state, c):
    sucs = []
    for i in range(sz):
        for j in range(sz):
            if state[i][j]=='':
                tmp = copy.deepcopy(state)
                tmp[i][j] = c
                sucs.append(tmp)
    return sucs;

#Alpha-Beta pruning algorithm
def alphabetasearch(state, cutoffdepth):
    fin,v = maxvalue(state,-1000,+1000,0,cutoffdepth)
    return fin

#MaxVal function for alpha-beta pruning
def maxvalue(state, alpha, beta, lvl, cutoffdepth):
    global nodesgenerated, maxdepth, prunedmax, prunedmin, cutoff
    nodesgenerated += 1
    lvl += 1
    if lvl>maxdepth:
        maxdepth = lvl

    #Return eval/utility when cutoff depth or terminal node reached
    best = None
    xs,os = evalf(state)
    if lvl >= cutoffdepth:
        cutoff = True
        return best, evalvalue(xs,os)

    if os[sz]==1:
        return best, +1000
    elif xs[sz]==1:
        return best, -1000
    elif isdraw(state):
        return best, 0

    #Look at next level(s)
    v = -99999
    for s in successors(state,'O'):
        st,m = minvalue(s, alpha, beta, lvl, cutoffdepth)
        if m>v:
            v = m
            best = s
        if v>=beta:
            prunedmax += 1
            return best,v
        alpha = max(alpha,v)

    return best,v

#MinVal function for alpha-beta pruning
def minvalue(state, alpha, beta, lvl, cutoffdepth):
    global nodesgenerated, maxdepth, prunedmax, prunedmin, cutoff
    nodesgenerated += 1
    lvl += 1
    if lvl>maxdepth:
        maxdepth = lvl
    
    #Return eval/utility when cutoff depth or terminal node reached
    best = None
    xs,os = evalf(state)
    if lvl >= cutoffdepth:
        cutoff = True
        return best, evalvalue(xs,os)

    if os[sz]==1:
        return best, +1000
    elif xs[sz]==1:
        return best, -1000
    elif isdraw(state):
        return best, 0
    

    #Look at next level(s)
    v = 99999
    for s in successors(state,'X'):
        st,m = maxvalue(s,alpha,beta,lvl,cutoffdepth)
        if m<v:
            v = m
            best = s
        if v<=alpha:
            prunedmin += 1
            return best,v
        beta = min(beta,v)

    return best,v


#Main game
gf = raw_input('Go first? y/n :  ')
player = True
if gf=='n':
    player = False
df = input('Difficulty 1,2,3 : ')

while True:
    
    #User(X - min player) input (x y)
    if player:
        print 'Player-X enter box (x y) - x to quit :',
        a = raw_input().split()
        if len(a)==1:
            break
        board[int(a[0])][int(a[1])] = 'X'

    else:
        print 'Player-O chooses: '
        if df>1:
            if df==2:
                #AI player for level-2 difficulty - alphabeta search with 3 move lookahead / cutoff depth
                board = alphabetasearch(board, 3)
            else:
                #AI player for level-3 difficulty - alphabeta search with 7 move lookahead / cutoff depth!
                board = alphabetasearch(board, 7)
            
            #Stats for alphabeta search
            print 'GenNodes, MaxPrune, MinPrune : ', nodesgenerated, prunedmax, prunedmin
            print 'MaxDepth, Cutoff? : ', maxdepth, cutoff
            nodesgenerated, prunedmin, prunedmax, maxdepth, cutoff = 0,0,0,0,False

        elif df==1:
            #AI player for level-1 difficulty - random move selection
            board = randompick(board)

    printboard(board)

    #Who won?
    xs,os = evalf(board)
    #print 'Eval : ', xs[1:], os[1:], evalvalue(xs,os)
    if os[sz]==1:
        print 'You lose!'
        break
    elif xs[sz]==1:
        print 'You win!'
        break
    elif isdraw(board):
        print 'Draw!'
        break

    player = not player


    

