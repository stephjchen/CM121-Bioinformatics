#Prompt: To save James Bond's reputation as a gambler, you must implement a prediction of whether the Casino Royale is cheating on every observed roll. You are given a spreadsheet of dice rolls and their probabilities under two models: F, "fair dice" where all rolls have equal probability (1/6); and L, "loaded dice" which rolls a 6 half the time, and any of the other rolls (1, 2, 3, 4, 5) with 10% probability each. The casino switches from F to L with 5% probability on each roll, and from L to F with 10% probability on each roll.
	
	#Emission Probabilities
	#P(1|F) = 1/6, P(2|F) = 1/6, ..., P(6|F) = 1/6
	#P(1|L) = 1/10, P(1|L) = 1/10, ..., P(5|L) = 1/10, P(6|L) = 1/2

	#Transition Probabilities
	#P(F|L) = 0.05, p(L|L) = 0.95
	#P(L|F) = 0.10, P(F|F) = 0.90

#Given the likelihood, a list of dice rolls, calculate the forward probability under two models– F (fair dice), and L (loaded dice)

#Input:
	# iks: a list of (p(roll|F), p(roll|L)) tuples, for each successive dice roll
	# ptrans: the transition matrix in the form ((p(F|F), p(L|F)), (p(F|L), p(L|L))
	# prior: a tuple of the prior probabilities (p(F), p(L))

	#Sample Input:
	# params,0.95,0.9,0.6666666666666666,0.3333333333333333
	# 6,0.16666666666666666,0.5
	# 1,0.16666666666666666,0.1
	# 1,0.16666666666666666,0.1
	# 2,0.16666666666666666,0.1
	# 6,0.16666666666666666,0.5

#Output:
	#forward probability f_F and f_L

	#Sample Output:
	# 0.1111111111111111,0.16666666666666666
	# 0.02037037037037037,0.015555555555555555
	# 0.003484567901234567,0.001501851851851852
	# 0.0005767541152263372,0.00015258950617283955
	# 9.386256001371738e-05,8.308413065843624e-05

def calc_forward(liks, ptrans, prior): # don't change this line
    '''liks is list of (p(roll|F), p(roll|L)); ptrans is p[from][to];
    prior is (p(F), p(L))'''
    
    #first element is (p(X1, theta1 = F), p(X1, theta1 = L))
    forward = [( liks[0][0]*prior[0],liks[0][1]*prior[1] )] # replace this with your calculation
    
    
    for i in range(1,len(liks)): #iterate through roll indexed 1-4
        #calculate f_F
        f_F = (forward[i-1][0]*ptrans[0][0] + forward[i-1][1]*ptrans[1][0])*liks[i][0]
        #calculate f_L
        f_L = (forward[i-1][0]*ptrans[0][1] + forward[i-1][1]*ptrans[1][1])*liks[i][1]
        forward.append((f_F, f_L))
        pass
    
    return forward

#Calculate backward probability b_F and b_L

	# Sample Input:
	# params,0.95,0.9,0.6666666666666666,0.3333333333333333
	# 2,0.16666666666666666,0.1
	# 6,0.16666666666666666,0.5
	# 2,0.16666666666666666,0.1
	# 1,0.16666666666666666,0.1
	# 6,0.16666666666666666,0.5

	# Sample Output:
	# 0.1111111111111111,0.03333333333333333,0.0009363167438271605,0.002146471450617284
	# 0.018148148148148146,0.01777777777777778,0.005190787037037037,0.0045776851851851855
	# 0.0031697530864197524,0.0016907407407407414,0.03136111111111111,0.04505555555555556
	# 0.0005300565843621397,0.00016801543209876552,0.18333333333333335,0.4666666666666667
	# 8.672588305898487e-05,8.8858359053498e-05,1.0,1.0

def calc_fb(liks, ptrans, prior): # don't change this line
    '''liks is list of (p(roll|F), p(roll|L)); ptrans is p[from][to];
    prior is (p(F), p(L))'''
    
    #backward = [(1.,1.)] # replace this with your calculation
    
    #calculate forward probability
    #first element is (p(X1, theta1 = F), p(X1, theta1 = L))
    forward = [( liks[0][0]*prior[0],liks[0][1]*prior[1] )] # replace this with your calculation
    for i in range(1,len(liks)): #iterate through roll indexed 1-4
        #calculate f_F
        f_F = (forward[i-1][0]*ptrans[0][0] + forward[i-1][1]*ptrans[1][0])*liks[i][0]
        #calculate f_L
        f_L = (forward[i-1][0]*ptrans[0][1] + forward[i-1][1]*ptrans[1][1])*liks[i][1]
        forward.append((f_F, f_L))
        pass
    
    num_rolls = len(liks)
    backward = [ [ 0 for y in range( 2 ) ] for x in range( num_rolls )]
    #calculate backward probability
    backward[num_rolls-1][0] = 1. # = backward[4][0] = b_F_4
    backward[num_rolls-1][1] = 1. # = backward[4][1] = b_L_4
    
    #traverse backward
    for i in range(num_rolls-2, -1, -1):
        #calculate b_F
        backward[i][0]=(backward[i+1][0]*ptrans[0][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[0][1]*liks[i+1][1])
        #calculate b_L
        backward[i][1]=(backward[i+1][0]*ptrans[1][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[1][1]*liks[i+1][1])
        pass
    
    return forward, backward

#Calculate p(obs), the likelihood by f_F * b_F + f_L * b_L
#p(obs) should be the same for each successive dice roll!

	# Sample Input:
	# params,0.95,0.9,0.6666666666666666,0.3333333333333333
	# 2,0.16666666666666666,0.1
	# 4,0.16666666666666666,0.1
	# 1,0.16666666666666666,0.1
	# 4,0.16666666666666666,0.1
	# 5,0.16666666666666666,0.1

	#Sample Output:
	# 0.1111111111111111,0.03333333333333333,0.0006791936882716048,0.000210080524691358,8.246864951989023e-05
	# 0.018148148148148146,0.003555555555555556,0.004240731481481481,0.0015489074074074073,8.246864951989025e-05
	# 0.0029327160493827155,0.0004107407407407409,0.026394444444444443,0.012322222222222222,8.246864951989023e-05
	# 0.00047119238683127556,5.163024691358028e-05,0.16333333333333333,0.10666666666666667,8.246864951989023e-05
	# 7.546596536351163e-05,7.0026841563786055e-06,1.0,1.0,8.246864951989023e-05

def calc_fb(liks, ptrans, prior): # don't change this line
    '''liks is list of (p(roll|F), p(roll|L)); ptrans is p[from][to];
    prior is (p(F), p(L))'''
    forward = [( liks[0][0]*prior[0],liks[0][1]*prior[1] )] # replace this with your calculation
    for i in range(1,len(liks)): #iterate through roll indexed 1-4
        #calculate f_F
        f_F = (forward[i-1][0]*ptrans[0][0] + forward[i-1][1]*ptrans[1][0])*liks[i][0]
        #calculate f_L
        f_L = (forward[i-1][0]*ptrans[0][1] + forward[i-1][1]*ptrans[1][1])*liks[i][1]
        forward.append((f_F, f_L))
        pass
    
    num_rolls = len(liks)
    backward = [ [ 0 for y in range( 2 ) ] for x in range( num_rolls )]
    #calculate backward probability
    backward[num_rolls-1][0] = 1. # = backward[4][0] = b_F_4
    backward[num_rolls-1][1] = 1. # = backward[4][1] = b_L_4
    
    #traverse backward
    for i in range(num_rolls-2, -1, -1):
        #calculate b_F
        backward[i][0]=(backward[i+1][0]*ptrans[0][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[0][1]*liks[i+1][1])
        #calculate b_L
        backward[i][1]=(backward[i+1][0]*ptrans[1][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[1][1]*liks[i+1][1])
        pass
    pobs = []
    for i in range(0, num_rolls):
        pobs.append(forward[i][0]*backward[i][0] + forward[i][1]*backward[i][1])

    return forward, backward, pobs

#get ppost: a list of (p(F|obs), p(L|obs)) posterior probability tuples for the F vs. L hidden state at each successive dice roll.

	# Sample Input:
	# params,0.95,0.9,0.6666666666666666,0.3333333333333333
	# 5,0.16666666666666666,0.1
	# 5,0.16666666666666666,0.1
	# 3,0.16666666666666666,0.1
	# 2,0.16666666666666666,0.1
	# 6,0.16666666666666666,0.5

	# Sample Output:
	# 0.1111111111111111,0.03333333333333333,0.0008447630401234568,0.0004985047839506174,0.00011047938614540466,0.8495934245161588,0.15040657548384123
	# 0.018148148148148146,0.003555555555555556,0.005190787037037037,0.0045776851851851855,0.00011047938614540466,0.8526764624637937,0.14732353753620628
	# 0.0029327160493827155,0.0004107407407407409,0.03136111111111111,0.04505555555555556,0.00011047938614540466,0.8324922602392261,0.1675077397607739
	# 0.00047119238683127556,5.163024691358028e-05,0.18333333333333335,0.4666666666666667,0.00011047938614540466,0.781913024076486,0.21808697592351392
	# 7.546596536351163e-05,3.5013420781893024e-05,1.0,1.0,0.00011047938614540466,0.6830773413620257,0.31692265863797425

def calc_fb(liks, ptrans, prior): # don't change this line
    '''liks is list of (p(roll|F), p(roll|L)); ptrans is p[from][to];
    prior is (p(F), p(L))'''
    forward = [( liks[0][0]*prior[0],liks[0][1]*prior[1] )] # replace this with your calculation
    for i in range(1,len(liks)): #iterate through roll indexed 1-4
        #calculate f_F
        f_F = (forward[i-1][0]*ptrans[0][0] + forward[i-1][1]*ptrans[1][0])*liks[i][0]
        #calculate f_L
        f_L = (forward[i-1][0]*ptrans[0][1] + forward[i-1][1]*ptrans[1][1])*liks[i][1]
        forward.append((f_F, f_L))
        pass
    
    num_rolls = len(liks)
    backward = [ [ 0 for y in range( 2 ) ] for x in range( num_rolls )]
    #calculate backward probability
    backward[num_rolls-1][0] = 1. # = backward[4][0] = b_F_4
    backward[num_rolls-1][1] = 1. # = backward[4][1] = b_L_4
    
    #traverse backward
    for i in range(num_rolls-2, -1, -1):
        #calculate b_F
        backward[i][0]=(backward[i+1][0]*ptrans[0][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[0][1]*liks[i+1][1])
        #calculate b_L
        backward[i][1]=(backward[i+1][0]*ptrans[1][0]*liks[i+1][0])+(backward[i+1][1]*ptrans[1][1]*liks[i+1][1])
        pass
    pobs = []
    for i in range(0, num_rolls):
        pobs.append(forward[i][0]*backward[i][0] + forward[i][1]*backward[i][1])
        
    ppost = [] #ppost: a list of (p(F|obs), p(L|obs))
    p_all = pobs[0]
    for i in range(0, num_rolls):
        p_F_obs = forward[i][0]*backward[i][0]/p_all
        p_L_obs = forward[i][1]*backward[i][1]/p_all
        ppost.append( (p_F_obs, p_L_obs) )
    
    return forward, backward, pobs, ppost
