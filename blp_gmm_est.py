from q1_prepdata import *
from scipy.optimize import minimize

# normal draws for simulatons, notice the all draws should be done in the begining
ndraws = np.random.normal(0,1,[nmarkets,3,1000]) #normal(0,1), 3 random char, 1000 draws
def simshare(deltaj,sig1,sig2,sigp): # predicted market share by simulations
	sims=[]
	sims_market=[]
	sims_m_e = []
	sim_marketshare = [0]*nprods
	sig=np.asarray([sig1,sig2,sigp])
	for m in range(0,nmarkets):
		mdenominator = 0 
		for j in range(marketpos[m][0],marketpos[m][1]+1):
			share = np.exp(deltaj[j]+np.multiply(randchar[j],sig)*ndraws[m])
			mdenominator += share
			sims.append(share)
		mdenominator += 1
		sims_market.append(mdenominator)
	sims=np.vstack(sims)
	sims_market=np.vstack(sims_market)
	for i in range(0, nprods):
		ind=prod_m[i]
		sim_marketshare[i] = np.average(np.asarray(sims[i])/np.asarray(sims_market[ind]))
	return np.reshape(sim_marketshare,(nprods,1))

def contraction(sig1,sig2,sigp): # contraction step to invert marketshare
	delta = [1]*nprods
	delta = np.reshape(delta,(nprods,1))
	delta1 = [0]*nprods
	delta1 = np.reshape(delta1,(nprods,1))
	absdiff = 1
	while (absdiff > 1e-13):
		delta1 = delta + np.log(mshare)-np.log(simshare(delta,sig1,sig2,sigp))
		absdiff = np.amax(abs(delta1-delta)) 
		delta=delta1
	
	return delta 

def gmm_blpobj(sigma):
	sig1 = sigma[0]
	sig2 = sigma[1]
	sig3 = sigma[2]
	# recover the linear parts of the parameters
	delta = contraction(sig1,sig2,sig3)
	theta1 = (X.T*pw*X).I*X.T*pw*delta
	 
	obj = (delta-X*theta1).T*pw*(delta-X*theta1) 
	#print theta1, sig
	return obj 



sig = [1.3,0.9,0.5]
min_val = minimize(gmm_blpobj,sig,method='Nelder-Mead')
#v1 = min_val['x'][0]
#v2 = min_val['x'][1]
#v3 = min_val['x'][2]
print min_val
#print gmm_blpobj(sig)

# Second step estimation starts here
#est_delta= contraction(1.16508818,  0.89854499,  0.30040452)
#est_theta1 = (X.T*pw*X).I*X.T*pw*est_delta
#est_omega = est_delta - X*est_theta1
#weight_gmm = np.matrix((instru1.T*est_omega*est_omega.T*instru1).I)


#def gmm_blpobj_2nd(sigma):
#	sig1 = sigma[0]
#	sig2 = sigma[1]
#	sig3 = sigma[2]
#	# recover the linear parts of the parameters
#	delta = contraction(sig1,sig2,sig3)
#	theta1 = (X.T*pw*X).I*X.T*pw*delta
	 
#	obj = (delta-X*theta1).T*instru1*weight_gmm*instru1.T*(delta-X*theta1) 
	#print theta1, sig
#	return obj 

#min_val = minimize(gmm_blpobj_2nd,sig,method='Nelder-Mead')

#print est_theta1

