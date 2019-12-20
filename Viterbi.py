#Implement Viterbi dynamic programming algorithm to calculate maximum alignment

#Input:
	# X, Y: the two sequences to align
	# S: the letter substitution score matrix, i.e. S['A']['G'] is the score for A vs. G
	# g: the gap penalty

	#Example:
	# CGTGCG,CAGTGG
	# -3,T,C,A,G
	# T,5,-2,-2,-2
	# C,-2,5,-2,-2
	# A,-2,-2,5,-2
	# G,-2,-2,-2,5

	#Here g (gap penalty) is -3, substitution score for mismatched letters is -2, for matched letters is 5

#Output:
	# a matrix scores, such that scores[t][u] is the optimal Viterbi score for the best possible alignment of the first t letters of sequence X vs. the first u letters of sequence Y.
	# a matrix moves, such that moves[t][u] is the optimal Viterbi move arriving at alignment matrix cell (t,u).

	#Example (output for above input):

	#scores:
	# 0,-3,-6,-9,-12,-15,-18
	# -3,5,2,-1,-4,-7,-10
	# -6,2,3,0,-3,-6,-9
	# -9,-1,7,4,5,2,-1
	# -12,-4,4,12,9,6,3
	# -15,-7,1,9,17,14,11
	# -18,-10,-2,6,14,15,19

	#moves:
	# 0,x,x,x,x,x,x
	# y,m,x,x,x,x,x
	# y,y,m,x,x,x,x
	# y,y,m,x,m,x,x
	# y,y,y,m,x,x,x
	# y,y,y,y,m,x,x
	# y,y,y,y,y,m,m


	def global_viterbi(X, Y, S, g): # do not change this line
    """X, Y are two sequences to align, S[L1][L2] is the substitution score, and g is the gap penalty"""
    # replace this with your actual calculation
    scores = [] # scores[t][u] = optimal score for aligning first t letters of X, u letters of Y
    moves = [] # moves[t][u] = optimal move for arriving at cell (t,u)

    rows, cols = (len(X)+1, len(Y)+1)
    scores = [[0 for i in range(cols)] for j in range(rows)] 
    moves = [[0 for i in range(cols)] for j in range(rows)] 
    cur_score = 0 #initial score at origin
    
    #inialization
    for i in range(cols):
        scores[0][i] = cur_score #each row at column 0
        moves[0][i] = 'y'
        scores[i][0] = cur_score #each column at row 0
        moves[i][0] = 'x'
        cur_score += g

    moves[0][0] = 0
        
    for x in range(0, cols-1):
        for y in range(0, rows-1):
            m_move = scores[x][y] + S[X[x]][Y[y]]
            x_move = scores[x][y+1] + g
            y_move = scores[x+1][y] + g
            score = max(m_move,x_move,y_move)
            scores[x+1][y+1] = score
            
            if score == y_move:
                moves[x+1][y+1] = 'y'
            elif score == x_move:
                moves[x+1][y+1] = 'x'
            else:
                moves[x+1][y+1] = 'm'
            
            
    return scores, moves

#Calculate the optimal global alignment by returning a list of aligned positions (t, u) for the best possible global alignment (sorted in ascending order) of sequence X vs. sequence Y
#Sample Input:
	# TCCGAA,CCGGTA
	# -3,A,G,C,T
	# A,5,-2,-2,-2
	# G,-2,5,-2,-2
	# C,-2,-2,5,-2
	# T,-2,-2,-2,5

#Sample Output:
	# 1,0
	# 2,1
	# 3,2
	# 4,3
	# 5,5


def align(X, Y, S, g): # do not change this line
    """X, Y are two sequences to align, S is scores[x][y] and g is the gap penalty"""
    
    scores = [] # scores[t][u] = optimal score for aligning first t letters of X, u letters of Y
    moves = [] # moves[t][u] = optimal move for arriving at cell (t,u)

    rows, cols = (len(X)+1, len(Y)+1)
    scores = [[0 for i in range(cols)] for j in range(rows)] 
    moves = [[0 for i in range(cols)] for j in range(rows)] 
    cur_score = 0 #initial score at origin
    
    #inialization
    for i in range(cols):
        scores[0][i] = cur_score #each row at column 0
        moves[0][i] = 'y'
        scores[i][0] = cur_score #each column at row 0
        moves[i][0] = 'x'
        cur_score += g

    moves[0][0] = 0
        
    for x in range(0, cols-1):
        for y in range(0, rows-1):
            #populate scores matrix
            m_move = scores[x][y] + S[X[x]][Y[y]]
            x_move = scores[x][y+1] + g
            y_move = scores[x+1][y] + g
            score = max(m_move,x_move,y_move)
            scores[x+1][y+1] = score
            
            #populate moves matrix
            if score == y_move:
                moves[x+1][y+1] = 'y'
            elif score == x_move:
                moves[x+1][y+1] = 'x'
            else:
                moves[x+1][y+1] = 'm'
  
    path = []
    i = cols-1
    j = rows-1
    traceback = moves[i][j]
    
    while i>0 and j>0:
        if traceback == 'm':
            i = i-1
            j = j-1
            path.append((i,j))
            #print('path(i, j)', (i, j))
        elif traceback == 'x':
            i = i-1
        else: #y_move
            j = j-1
    
    
    path.sort() # replace this with your actual calculation
    return path




