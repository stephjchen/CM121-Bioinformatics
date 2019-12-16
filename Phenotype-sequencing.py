#Identify the genes that cause a mutant phenotype
#Calculate probability of an observed number of mutations in a gene given its expected number of mutations under the non-target gene model p(k | lambdaMean), assuming a Poisson model

#Input: geneData is a list of (lambdaMean, k, geneID) tuples where lambdaMean is the expected number of mutations under the non-target gene model for this gene, k is the number of mutations actually observed in this gene in this phenotype sequencing experiment, and geneID is the identifier string for this gene.
#Example:
	# 0.08475427497628685,3,0
	# 0.07069642463513282,0,1
	# 0.6723278444175941,5,2
	# 0.2216668161686599,6,3
	# 0.8280870824979073,11,4

#Output: a list of (p(k|lambdaMean, geneID) tuples
#Example:
	# 9.32234722699e-05,0
	# 0.931744703937,1
	# 0.000584434669005,2
	# 1.32008814051e-07,3
	# 1.37418986758e-09,4

from scipy import stats
def calc_nontarget_probs(geneData):  # do not modify this line
    'geneData is list of (lambdaMean, k, geneID) tuples'
    hits = [] # insert your calculation here
    for x in geneData:
        p = stats.poisson.pmf(x[1], x[0])
        hits.append((p,x[2])) #x[2] is geneID
    return hits # should be list of (p(k|lambdaMean), geneID) tuples


#Calculate the p-value (p(K >= k | lambdaMean), the ﻿probability of getting the observed number of mutations in a gene or more) given its expected number of mutations under the non-target gene model, assuming a Poisson model

#Input: geneData is a list of (lambdaMean, k, geneID) tuples where lambdaMean is the expected number of mutations under the non-target gene model for this gene, k is the number of mutations actually observed in this gene in this phenotype sequencing experiment, and geneID is the identifier string for this gene.
#Example:
	# 0.08475427497628685,3,0
	# 0.07069642463513282,0,1
	# 0.6723278444175941,5,2
	# 0.2216668161686599,6,3
	# 0.8280870824979073,11,4

#Output: a list of (p(K >= k|lambdaMean), geneID) tuples
#Example:
	# 0.00769514703064,0
	# 4.66853685005e-09,1
	# 9.98372271255e-11,2
	# 0.016927805155,3
	# 8.69929837843e-07,4

def calc_nontarget_pvals(geneData):  # do not modify this line
    'geneData is list of (lambdaMean, k, geneID) tuples'
    hits = [] # insert your calculation here
    for x in geneData:
        p_sum = 0
        k = x[1]
        for i in range(0,k):
            p_sum += stats.poisson.pmf(i, x[0])
        p = 1 - p_sum
        hits.append((p, x[2]))
    
    return hits # should be list of (p(K >= k|lambdaMean), geneID) tuples


#Calculate the probability of an observed number of mutations in a gene given the size of that gene (in arbitrary units), p(k | size), assuming a Poisson model with an expected number of mutations simply proportional to the gene's length (size)

#Input: geneData is list of (size, k, geneID) tuples where size is the length of this gene, k is the number of mutations actually detected in this gene in this phenotype sequencing experiment, and geneID is the identifier string for this gene
#Example:
	# 0.620536252468985,5,0
	# 0.8406851112124463,7,1
	# 0.49726340075100606,4,2
	# 0.6910376152199857,8,3
	# 0.5191937840238267,5,4

#Output: a list of (p(k|lambdaMean), geneID) tuples
#Example:
	# 0.168194960377,0
	# 0.144269951409,1
	# 0.188688331096,2
	# 0.113756729137,3
	# 0.174351433496,4

def calc_varsize_probs(geneData):  # do not modify this line
    'geneData is list of (size, k, geneID) tuples'
    hits = [] # insert your calculation here
    s_all = 0
    k_all = 0
    for x in geneData:
        s_all += x[0] #get total size of genome
        k_all += x[1] #get total number of mutations
    
    lamda_const = k_all/s_all
    for x in geneData:
        lamda = lamda_const*x[0]
        p = stats.poisson.pmf(x[1],lamda)
        hits.append((p, x[2]))
        
    
    return hits # should be list of (p(k|lambdaMean), geneID) tuples


#Calculate p-value given the size of that gene (in arbitrary units), p(K >= k | size), assuming a Poisson model

#Input: geneData is list of (size, k, geneID) tuples where size is the length of this gene, k is the number of mutations actually detected in this gene in this phenotype sequencing experiment, and geneID is the identifier string for this gene
#Example:
	# 0.672407534445396,9,0
	# 0.09422427989868787,1,1
	# 0.32651163950520945,4,2
	# 0.09053033936480082,0,3
	# 0.9752702957437336,12,4

#Output: a list of (p(K >= k|lambdaMean), geneID) tuples
#Example:
    # 7.53041910425e-29,330
    # 0.000857841715704,359
    # 0.0208477425543,362
    # 0.0248199610653,32
    # 0.0267729361894,226

def calc_varsize_pvals(geneData):  # do not modify this line
    'geneData is list of (size, k, geneID) tuples'
    hits = [] # insert your calculation here
    s_all = 0
    k_all = 0
    for x in geneData:
        s_all += x[0] #get total size of genome
        k_all += x[1] #get total number of mutations = N
    lamda_const = k_all/s_all
    
    for x in geneData:
        p_sum = 0
        k = x[1]
        for i in range(0,k):
            p_sum += stats.poisson.pmf(i, x[0]*lamda_const)
        
        p = 1-p_sum
        hits.append((p,x[2]))
        
    return hits # should be list of (p(K >= k|lambdaMean), geneID) tuples

#Calculate p-value given the size of that gene (in arbitrary units) under a Poisson model, output results to report only predicted positives such that at most one false positive (over the whole genome) would be expected on average, using the Bonferroni correction.
#Also report the alpha cutoff value used for filtering.

#Input: geneData is list of (size, k, geneID) tuples where size is the length of this gene, k is the number of mutations actually detected in this gene in this phenotype sequencing experiment, and geneID is the identifier string for this gene
#Example:
	# 0.829201211571918,2,0
	# 0.7168270320056007,1,1
	# 0.05243891730041028,0,2
	# 0.834730396452797,3,3
	# 0.4135796763224442,2,4
	
#Output: predicted positives such that at most one false positive (over whole genome) would be expected given size and observed k, and the alpha value used in the nextline
#Example:
    # 2.89112084319e-28,64
    # 0.0025,ALPHA

def get_sorted_hits(geneData): # do not modify this line
    """geneData is list of (size, k, gene) tuples"""
    hits_all = [] # replace this with your actual calculation
    s_all = 0.0
    N = 0.0
    for x in geneData:
        s_all += x[0] #get total size of genome
        N += x[1] #get total number of mutations = N = k_all
    alpha = 1./len(geneData)
    for x in geneData:
        p = stats.poisson.sf(x[1]-1, N*(x[0]/s_all))
        hits_all.append( (p,x[2]) )
    
    hits = [x for x in hits_all if x[0] <= alpha]
    return hits, alpha




