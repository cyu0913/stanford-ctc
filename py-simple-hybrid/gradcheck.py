import nnet as nnet
import gnumpy as gp
import numpy as np
from random import sample

def gradcheck(model, times=None, *args):
    """
    Gradient check for model.
    model should at least implement two methods:

        costAndGradVec(param, *args) - takes a vectorized parameter and computes cost and Gradient
        paramVec() - gets the model parameters collectively in a vector
    """
    param = model.paramVec()
    if (times == None or times > len(param)): times = len(param)
    ind = sample(xrange(len(param)), times)
    epsilon = 1e-4

    print "Iter\tIndex\tNumGrad\t\tGrad\t\tDiff"

    for time in range(times):
        index = ind[time]
        _,grad = model.costAndGradVec(param,*args)
        grad = grad[index]

        param_p = np.array(param)
        param_p[index] += epsilon
        cost_p,_ = model.costAndGradVec(param_p,*args)

        param_m = np.array(param)
        param_m[index] -= epsilon
        cost_m,_ = model.costAndGradVec(param_m,*args)

        numgrad = (cost_p - cost_m) / epsilon / 2

        diff = abs(numgrad - grad)

        print "%d\t%d\t%1.5e\t%1.5e\t%1.5e" % (time+1,index,numgrad,grad,diff)

        if (diff > 1e-4):
            print ("GradCheck failed, returning early. Check the last line of output for details.")
            return

class gradcheckCheck:
    def __init__(self, param):
        self.param = param

    def costAndGradVec(self, param):
        return np.sum(np.array(param) ** 2), 2*np.array(param)

    def paramVec(self):
        return self.param

if __name__=='__main__':

    # gcc = gradcheckCheck(np.random.rand(10,1))
    # gradcheck(gcc)

    inputDim = 5
    outputDim = 10
    layerSizes = [3,3]
    mbSize = 5

    # fake data
    data = gp.rand(inputDim,mbSize)
    import random
    labels = [random.randint(0,9)]*mbSize

    # make nnet
    nn = nnet.NNet(inputDim,outputDim,layerSizes,mbSize,train=True)
    nn.initParams()

    # run
    gradcheck(nn, 1000, data, labels)