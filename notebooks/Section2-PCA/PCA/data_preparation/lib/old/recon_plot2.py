import numpy as np
from YearPlotter import YearPlotter
from Eigen_decomp import Eigen_decomp
import matplotlib.pyplot as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

def compute_var(vector):
    v=np.array(np.nan_to_num(vector),dtype=np.float64)
    return np.dot(v,v)
 
class recon_plot:
    """A class for creating an interactive demonstration of approximating 
    a function with an orthonormal set of function"""
    def __init__(self,eigen_decomp,year_axis=False):
        """ 
        Initialize the plot widget
        :param: eigen_decomp: An Eigen_Decomp object
        :param: year_axis: set to true if X axis should correspond to the months of the year.

        """
        self.eigen_decomp=eigen_decomp
        #self.C=eigen_decomp.C
        #self.coeff=eigen_decomp.coeff
        #self.mean=eigen_decomp.mean
        
        self.year_axis=year_axis
        self.yearPlotter=None
        if year_axis:
            self.yearPlotter=YearPlotter()
        self.plot_combination(**self.eigen_decomp.coeff)
        return None

    def get_widgets(self):
        """return the slider widget that are to be used

        :returns: widget_list: the list of widgets in order
                  widget_dict: a dictionary of the widget to be used in `interact

        :todo: make the sliders smaller: http://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Styling.html
        """
        coeff=self.eigen_decomp.C
        widge_dict={}
        widge_list=[]
        for i in range(self.eigen_decomp.n):
            if coeff[i]>0:
                r=[0,coeff[i]*2]
            else:
                r=[coeff[i]*2,0]

            widge_list.append(widgets.FloatSlider(min=r[0],max=r[1],step=coeff[i]/10.,\
                                                  value=coeff[i],orientation='vertical',decription='v'+str(i)))
            widge_dict['c'+str(i)]=widge_list[-1]

        return widge_list,widge_dict

    def plot(self,y,label=''):
        if self.year_axis:
            self.yearPlotter.plot(y,self.fig,self.ax,label=label)
        else:
            self.ax.plot(self.eigen_decomp.x,y,label=label);

    def plot_combination(self,**coeff):
        """the plotting function that is called by `interactive`
           generates the plot according the the parameters set by the sliders

        :returns: None
        """
        
        A=self.eigen_decomp.mean
        self.fig=plt.figure(figsize=(8,6))
        self.ax=self.fig.add_axes([0,0,1,1])
        self.plot(A,label='mean')

        for i in range(self.eigen_decomp.n):
            g=self.eigen_decomp.v[i]*coeff['c'+str(i)]
            A=A+g
            self.plot(A,label='c'+str(i))
        self.plot(self.eigen_decomp.f,label='target')
        self.ax.grid(figure=self.fig)        
        self.ax.legend()
        return None
    