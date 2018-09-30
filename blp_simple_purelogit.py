from q1_prepdata import *
from scipy.optimize import minimize


def gmmobj(b):
	b1=b[0]
	b2=b[1]
	b3=b[2]
	b4=b[3]
	a=b[4]
	beta = np.matrix(np.vstack([b1,b2,b3,b4,a]))
	gmmobj = (meanutil-X*beta).T*pw*(meanutil-X*beta)
	return gmmobj

# The following code use minimization routine to find the estimates
x0 = [1,1,1,1,1]
min_val = minimize(gmmobj,x0,method='BFGS')
#print min_val["x"]
#print beta_plogit 

# Initial GMM estimate
pw = instru1*(instru1.T*instru1).I*instru1.T
X = np.hstack([char,price])
beta_plogit = (X.T*pw*X).I*X.T*pw*meanutil

#print beta_plogit 

# Calculate efficient GMM with feasible HCCME.

res = np.asarray(meanutil - X*beta_plogit)
utsq = np.diag(np.hstack(np.multiply(res,res))) # need hstack before make diagonal
weight = instru1.T*utsq*instru1
beta_efgmm = (X.T*instru1*weight.I*instru1.T*X).I*X.T*instru1*weight.I*instru1.T*meanutil
var_fgmm = (X.T*instru1*weight.I*instru1.T*X).I
print np.hstack([beta_efgmm, np.vstack(np.sqrt(np.diag(var_fgmm)))])


