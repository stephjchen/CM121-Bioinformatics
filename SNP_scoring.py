#Compute log odds ratio for 2 models–– SNP v.s. No-SNP at a candidate SNP site
#Assumption: population allele frequency of 20% under SNP model, each read is drawn from a large pooled population sample, i.e. each read is independent, drawn from a different person

#Input: basecall likelihood under SNP(S) and No-SNP(S') model for each read
#Assume real SNPs occur on average at one in a thousand positions in the genome

#Sample Input: 0.001,0.99, 1
#Sample Output: -1.6144554844260801

import math
def calc_snp_log_odds(readData): # do not modify this line
    """readData is a list of (p(read|S), p(read|S'), readID) tuples """
    odds = 0.001/0.999
    for x in readData:
        odds *= (x[0]*0.8 + x[1]*0.2)/x[0]
    logOdds = math.log(odds) # replace this with your actual calculation
    return logOdds


#Use code below to handle big datasets
#Hint: the IEEE floating point standard cannot represent positive numbers smaller than around 10-200 (i.e. it silently truncates them to zero), which can lead to both wrong results and math domain errors. Robust probability calculations on big datasets require doing the calculations using log-probabilities (i.e. log10_p=-200 instead of p=1e-200), e.g. log_p=log_p1+log_p2 instead of p=p1*p2.

import math
def calc_snp_log_odds(readData): # do not modify this line
    """readData is a list of (p(read|S), p(read|S'), readID) tuples """
    odds_num = 0 #math.log(0.001) #p(SNP)
    odds_den = 0 #math.log(0.999) #p(No-SNP)
    for x in readData:
        odds_num += math.log(x[0]*0.8 + x[1]*0.2) #theta = 0.2
        odds_den += math.log(x[0]) #theta = 0
    logOdds = math.log(0.001) + odds_num - math.log(0.999) - odds_den # replace this with your actual calculation
    return logOdds