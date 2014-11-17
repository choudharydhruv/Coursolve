__author__='Dhruv Choudhary'


import numpy as np


class NonNegativeMatrixFactorization(object):

    """
    Non negative matrix factorization with two loss functions using multipicative-additive rules

    Params
        loss = sq or kl
    
        V = The user-item or item=item matrix to be factored  (N x M)

        r = Number of communities to be formed

    Returns
        W = each column is a cluster centroid of factored data (N x r)
	
	H = Users membership to the cluster centroids

        Every column of V: v = Wh, is a linear combination of columns of W weighted by column h

    """

    def __init__(self, loss='kl', r=10, epsilon=1e-6): 
        self.loss =  loss
	self.r = r
	self.e = epsilon

    def fit(self,V, iterations=200, debug=False):
        self.V = V
	r = self.r
	eps = self.e

        N,M = V.shape

        initValue = V.mean()

	if debug==True:
	    print V 

        Winit = np.random.rand(N,r) * initValue
        Hinit = np.random.rand(r,M) * initValue    


        W = np.maximum(Winit, eps)
        H = np.maximum(Hinit, eps)

        WdotH = W.dot(H) + eps
        VbyWH = V / WdotH + eps

	if debug==True:
	    print WdotH
	    print VbyWH

        for i in range(iterations):
            H *= (np.dot(VbyWH.T, W) / W.sum(axis=0)).T
	    H = np.maximum(H, eps)

            WdotH = W.dot(H) + eps
            VbyWH = V / WdotH + eps
            W *= np.dot(VbyWH, H.T) / H.sum(axis=1)
	    W = np.maximum(W, eps)

            WdotH = W.dot(H) + eps
            VbyWH = V / WdotH + eps

	    if debug==True and iterations%20 == 0:
	        print WdotH
	        print VbyWH

            divergence = ((V * np.log(VbyWH)) - V + WdotH).sum()
            print("At iteration {i}, the Kullback-Liebler divergence is {d}".format(i=i, d=divergence))
	    if debug==True and iterations%10 == 0:
	        print "Reconstructed matrix ", WdotH
        
        self.W = W
        self.H = H
        return W,H

if __name__=='__main__':

    model = NonNegativeMatrixFactorization('kl', 6)

    V = np.arange(.01,1.01, 0.01).reshape(10,10)   

    W,H = model.fit(V)

    print W,H
    print 'Original matrix', V
    print 'factored reconstruction', W.dot(H)
