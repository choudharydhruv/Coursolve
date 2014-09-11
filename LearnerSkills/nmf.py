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

    def __init__(self, loss=kl, r) 
        self.loss =  loss
	self.r = r

    def fit(self,V):
        self.V = V
        #Dimensions        
        self.N = V.shape[0]
        self.M = V.shape[1]

        initValue = V.mean()
 
        Winit = np.random.random(N*r).reshape(N, r) * avg_V
        Hinit = np.random.random(r*M).reshape(r, M) * avg_V        

        W = Winit
        H = Hinit

        WdotH = W.dot(H)
        VbyWH = V / WdotH

        for i in range(iterations):
            H *= (np.dot(VbyWH.T, W) / W.sum(axis=0)).T

            WdotH = W.dot(H)
            VbyWH = V / WH
            W *= np.dot(VbyWH, H.T) / H.sum(axis=1)

            WdotH = W.dot(H)
            VbyWH = V / WdotH

            divergence = ((V * np.log(V_over_WH)) - V + WH).sum()
            print("At iteration {i}, the Kullback-Liebler divergence is {d}".format(
                i=i, d=divergence))
        
        self.W = W
        self.H = H


