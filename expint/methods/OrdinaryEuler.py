from expint.methods.Method import Method
import scipy.sparse.linalg as sl
import numpy as np

class ExplicitEuler(Method):
    def __init__(self,rhs=None):
        super(ExplicitEuler,self).__init__(rhs)
    
    @classmethod
    def name(self):
        return "ExplicitEuler"
    
    def integrate(self, x0, t0, tend, N=100):
        h = np.double(tend-t0)/N
        t = np.zeros((N+1,1)); t[0]=t0
        x = x0; y = [x0]
        for i in xrange(N):
            x = x + h*self.rhs.Applyf(x)
            y.append(x)
            t[i+1] = t[i]+h
        return t,np.array(y)

# TODO: re-code this to make more sense (was used to test something..)
class ImplicitEuler(Method):
    @classmethod
    def name(self):
        return "ImplicitEuler"
    
    def __init__(self,rhs=None):
        super(ImplicitEuler,self).__init__(rhs)
        if not hasattr(rhs,'M') or not hasattr(rhs,'A') or not hasattr(rhs,'F'):
            raise Exception("This Integrator only works for RHS classes with attributes A,M and F.\n A: stiffness matrix, M: mass matrix, F: (constant) load vector")
    
    def integrate(self, y0, t0, tend, N=100, abstol=1e-5, reltol=1e-5):
        M = self.rhs.M
        A = self.rhs.A
        F = self.rhs.F
        h = np.double(tend-t0)/N
        t = np.zeros((N+1,1)); t[0]=t0
        x = y0.copy(); y = [y0.copy()]
        for i in xrange(N):
            x = sl.linsolve.spsolve(M+h/2*A,F*h+(M-h/2*A)*x)
            y.append(x)
            t[i+1] = t[i] + h
        return t,np.array(y)

