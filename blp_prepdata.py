import numpy as np
import scipy.io as sio
import itertools

data = sio.loadmat("demand_data.mat")
market = data["prodsMarket"]-1 # the -1 is to adjust position in an array (array starts at 0)
mshare = data["share"]
char = data["ch"]
cost = data["costShifters"]
firm = data["f"]
price = data["pr"]
nprods = firm.size # number of different products

# Get the market shares for the outside good in each market. #
outside = []
marketpos = []
startpos = 0
endpos = 0
for pos in market:
	endpos = startpos+pos
	marketpos.append([startpos, endpos])
	tshare = sum(mshare[startpos:endpos+1]) # note the +1 (range does not include last element)
	outside.append(1-tshare)
	startpos = endpos + 1
###############################################################

outside = np.asarray(outside) # shares of outside good in each market
marketpos= np.asarray(marketpos) # staring and ending position os each market in the market array
nmarkets = marketpos.shape[0] # number of different markets

# Now calculate mean utility for each good #
outshare = []
prod_m = []
for n in range(0,market.size): # expand outside share into 247 by 1 matrix
	o=np.repeat(outside[n], market[n]+1)
	p_m = np.repeat(n,market[n]+1)
	prod_m.append(p_m)	
	outshare.append(o)

prod_m = np.hstack(np.asarray(prod_m))
outshare = np.matrix(np.hstack(np.asarray(outshare))).T
meanutil = np.log(mshare)-np.log(outshare)
 
###############################################################


# Create the BLP instruments #
blp_instr1 = []
for p in range(0,firm.size):
	blp1 = 0
	blp2 = 0
	blp3 = 0
	blp4 = 0
	blp5 = 0
	blp6 = 0
	blp7 = 0
	blp8 = 0
	firmid = firm[p] # get which firm produce  p
	m = prod_m[p]
	for j in range(marketpos[m][0],marketpos[m][1]+1):
		if ((firm[j] == firmid) and (p !=j)):
				blp1 += char[j][0]
				blp2 += char[j][1]
				blp3 += char[j][2]
				blp4 += char[j][3]
		if (firm[j] != firmid):
				blp5 += char[j][0]
				blp6 += char[j][1]
				blp7 += char[j][2]
				blp8 += char[j][3]
	blp_instr1.append([blp1,blp2,blp3,blp4,blp5,blp6,blp7,blp8])
	

	


blp_instr1=np.asarray(blp_instr1)
instru1 = np.hstack([np.matrix(char), np.matrix(blp_instr1), np.matrix(cost)])

# optimal weighting matrix for GMM (pure logit)
pw = instru1*(instru1.T*instru1).I*instru1.T

# stacked charatertics and price
X = np.hstack([char,price])


# charateristics that have random coefficients
randchar = np.hstack([np.matrix(char[:,0]).T,np.matrix(char[:,1]).T, -price])
