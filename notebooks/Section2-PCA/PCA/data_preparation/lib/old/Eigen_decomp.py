import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets
 
class Eigen_decomp:
    """A class for approximating a function with an orthonormal set of
    functions    """
    
    def __init__(self,x,f,mean,U):
        """ Initialize the widget

        :param x: defines the x locations
        :param f: the function to be approximated
        :param mean: The initial approximation (the mean)
        :param U: an orthonormal matrix with m columns (number of vectors to use in decomposition)
        :returns: None
        """

        self.U=U
        
        self.x=x
        self.mean=mean

        self.f=f
        self.startup_flag=True
        #print('Eigen Decomp:',type(self.U),self.U.shape)
        
        self.C=np.dot((np.nan_to_num(f-mean)),self.U)  # computer the eigen-vectors coefficients.
        self.C=np.array(self.C).flatten()
        self.m,self.n=np.shape(self.U)
        self.coeff={'c'+str(i):self.C[i] for i in range(self.C.shape[0])} # Put the coefficient in the dictionary format that is used by "interactive".
        return None

    def compute_var_explained(self):
        """Compute a summary of the decomposition

        :returns: ('total_energy',total_energy),
                ('residual var after mean, eig1,eig2,...',residual_var[0]/total_energy,residual_var[1:]/residual_var[0]),
                ('reduction in var for mean,eig1,eig2,...',percent_explained[0]/total_energy,percent_explained[1:]/residual[0]),
                ('eigen-vector coefficients',self.C)

        :rtype: tuple of pairs. The first element in each pair is a
        description, the second is a number or a list of numbers or an
        array.

        """
        def compute_var(vector):
            v=np.array(np.nan_to_num(vector),dtype=np.float64)
            return np.dot(v,v) # /float(total_variance)
        
        k=self.U.shape[1]
        residual_var=np.zeros(k+1)
        
        residual=self.f   # init residual to function 
        total_energy=compute_var(residual)
        residual=residual-self.mean # set residual to function - mean 
        residual_var[0]=compute_var(residual)
        # compute residuals after each 
        for i in range(k):
            g=self.U[:,i]*self.coeff['c'+str(i)]
            g=np.array(g).flatten()
            residual=residual-g # subtract projection on i'th coefficient from residual
            residual_var[i+1]=compute_var(residual)

        # normalize residuals
        _residuals=residual_var/residual_var[0]   # Divide ressidulas by residuals after subtracting mean
        _residuals[0] = residual_var[0]/total_energy

        return (('total_energy',total_energy),
                ('fraction residual var after mean, eig1,eig2,...',_residuals),
                ('eigen-vector coefficients',self.coeff))

    # total_var,residuals,reductions,coeff=recon.compute_var_explained()
