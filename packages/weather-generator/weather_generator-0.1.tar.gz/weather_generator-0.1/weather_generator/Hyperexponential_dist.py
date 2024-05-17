"""
    Modified on May 11, 2024
    @author: Farafehizoro Ramanjatonirina

"""
from scipy.stats import rv_continuous
import numpy as np
from scipy.optimize import minimize

class Hyperexp(rv_continuous):
    """
    Class for the hyperexponential distribution, with k = 2.
    I.E. : sum of two exponential distribution. 
    pdf = p1 * beta1 * exp(-x*beta1) + (1-p1) * beta2 * exp(-x*beta2)
    
    Attributes: 
        p1: between 0 and 1
        beta1 > 0
        beta2 > 0
    """
    def _pdf(self, x, p1, beta1, beta2):
        """
        the probability distribution function
        """
        pdf1 = p1 * beta1 * np.exp(-beta1*x) 
        pdf2 = (1-p1) * beta2 * np.exp(-beta2 * x)
        return pdf1 + pdf2 
    
    def _cdf(self, x, p1, beta1, beta2): 
        """
        the cumulative distribution function
        """
        cdf1 = p1 * (1-np.exp(-beta1*x))
        cdf2 = (1-p1) * (1-np.exp(-beta2*x))
        return  cdf1 + cdf2
        
    def _logpdf(self, x, p1, beta1, beta2):
        """
        the log pdf
        """
        log_pdf1 = np.log(p1) + np.log(beta1) - beta1*np.array(x)
        log_pdf2 = np.log(1-p1) + np.log(beta2) - beta2*np.array(x)
        return np.logaddexp(log_pdf1, log_pdf2)
        
    def fit(self, data):
        """
        the fitting of the hyperexponential distribution
        """
        def neg_log_likelihood(params):
            p1, beta1, beta2 = params
            if not (0 < p1 < 1 and beta1 > 0 and beta2 > 0):
                return np.inf
           
            log_likelihood = - np.sum(self._logpdf(data, p1, beta1, beta2))
            return log_likelihood
        #initial_guess = [0.5, 1, 1]
        initial_guess = [0.4, 1,0.3]
        result = minimize(neg_log_likelihood, initial_guess)
        #print(result.x)
        res_p, res_beta1, res_beta2 = result.x
        return res_p, res_beta1, res_beta2