"""
    Modified on May 11, 2024
    @author: Farafehizoro Ramanjatonirina

"""

from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import math
from scipy import stats
from scipy.optimize import minimize
import warnings
import random
from .Hyperexponential_dist import Hyperexp

class Rain_WeatherGenerator():
    """
    Class to generate stochastically daily rainfall 
    Attributes: 
        * None
    
    """
    def __init__(self): 
        self.data = []
        self.data_df = pd.DataFrame(columns=['Year', 'Month', 'Day', 'RR', 'rainy_d', 'rainy_d1', 'rainy_d2'])
        self.start_date = datetime(1991,1,1)
        self.end_date = datetime(2020,12,31)
        self.date_list = []
        self.rain_occ_model = "1_order" #can be 1_order, 2_order, mixed_order
        self.rain_quantity_model = "weibull" #hyperexponential, exponential, weibull, gamma, exponential
        self.M1 = []
        self.M2 = []
        self.prob0 = []
        self.fit_expon = []
        self.fit_weibull = []
        self.fit_gamma = []
        self.fit_hyperexpon = []
        self.model_fitted = False
        
    def import_data(self, data_list, start_date, end_date): 
        """
        Import the data to fit the weather generator model
        
        Parameters
        ----------
        data_list : daily precipitation data
        start_date: the first day in the data
        end_date = the last day in the data
            
        Returns
        -------
        none

        """
    
        self.start_date = datetime.strptime(start_date,  "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date,  "%Y-%m-%d")
        self.date_list = pd.date_range(self.start_date, self.end_date )
        
        if isinstance(data_list, pd.Series):
            data_list = data_list.tolist()
        self.data = data_list    
        rr_c = [NaN if u == -99 else u for u in self.data ]
        temporary = [1 if u > 0 else 0 for u in rr_c]
        rainy_d = [pd.NA if math.isnan(u) else v for u, v in zip(rr_c, temporary)]
        rainy_d1 = rainy_d[0: len(rainy_d)-1]
        rainy_d1.insert(0, pd.NA)
        rainy_d2 = rainy_d1[0: len(rainy_d1)-1]
        rainy_d2.insert(0, pd.NA)
        
        self.data_df = pd.DataFrame({'Year': self.date_list.year, "Month": self.date_list.month, "Day": self.date_list.day, 
                                     "RR": rr_c, "rainy_d": rainy_d, "rainy_d1" : rainy_d1, "rainy_d2": rainy_d2})
        self.fit_model()
       
   
    def fit_model(self): 
        """
        Estimate the parameter of the weather generator for all month
        
        Parameters
        ----------
        None
            
        Returns
        -------
        none

        """
        #reinitialize all the data
        self.M1 = []
        self.M2 = []
        self.prob0 = []
        self.fit_expon = []
        self.fit_weibull = []
        self.fit_gamma = []
        self.fit_hyperexpon = []
        self.model_fitted = False
        for m in np.arange(12):
            mo = m + 1
            df_rrm = self.data_df.query('Month == @mo')
            df_rrm2 = df_rrm.reset_index(drop=True)
            ind = pd.notna(df_rrm2.loc[:, "rainy_d"])
            ind1 = pd.notna(df_rrm2.loc[:, "rainy_d1"])
            ind2 = pd.notna(df_rrm2.loc[:, "rainy_d2"])
            
            ind_tot = [u and v and w for u, v, w in zip(ind, ind1, ind2)]

            df_rrm3 = df_rrm[ind_tot]
            df_rrm3 = df_rrm3.reset_index(drop=True)
            
            iM1 = [pd.NA, pd.NA]
            iM2 = [pd.NA, pd.NA, pd.NA, pd.NA]

            w1 = df_rrm3.query('rainy_d1 == 1')
            d1 = df_rrm3.query('rainy_d1 == 0')

            iM1[0] = 1 - d1.rainy_d.sum() / len(d1)
            iM1[1] = 1 - w1.rainy_d.sum() / len(w1)

            w2 = df_rrm3.query('rainy_d2 == 1')
            d2 = df_rrm3.query('rainy_d2 == 0')

            d2d = d2.query('rainy_d1 == 0')
            d2w = d2.query('rainy_d1 == 1')
            w2d = w2.query('rainy_d1 == 0')
            w2w = w2.query('rainy_d1 == 1')

            iM2[0] = 1 - d2d.rainy_d.sum() / len(d2d) if len(d2d) > 0 else 0 
            iM2[1] = 1 - d2w.rainy_d.sum() / len(d2w)
            iM2[2] = 1 - w2d.rainy_d.sum() / len(w2d)
            iM2[3] = 1 - w2w.rainy_d.sum() / len(w2w) if len(w2w) > 0 else 1 

            iprob0 = 1 - df_rrm3.rainy_d.sum() / len(df_rrm3)

            for l in np.arange(0,4):
                if iM2[l] < 0.01:
                    iM2[l] = 0.01
                    continue
                if iM2[l] > 0.99: 
                    iM2[l] = 0.99
            
            self.M1.append(iM1)
            self.M2.append(iM2)
            self.prob0.append(iprob0)
            #fit rain model
            rr_day = [u for u in df_rrm2.RR if u > 0]
            fitw = stats.weibull_min.fit(rr_day, floc = 0)
            fite = stats.expon.fit(rr_day, floc = 0)
            fitg = stats.gamma.fit(rr_day, floc = 0) 
            hyper_d = Hyperexp()
            warnings.filterwarnings("ignore", message="invalid value encountered in subtract")
            fith = hyper_d.fit(rr_day )
            
            self.fit_expon.append(fite)
            self.fit_weibull.append(fitw)
            self.fit_gamma.append(fitg)
            warnings.filterwarnings("ignore", message="invalid value encountered in subtract")
            self.fit_hyperexpon.append(fith)
        self.model_fitted = True
        
    def run_weath_gen(self, year, month, nb_real, rain_occ_model= "1_order", rain_quant_model= "weibull"): 
        """
        run the stochastic weather generator to generate daily data for a specific month, 
        
        Parameters
        ----------
            *year: year of the data to be generated
            *month: month of the data to be generated
            *nb_real: number of instance
            *rain_occ_model: the model of rain occurrence 
                # 1_order: first  order markov chain (default value)
                # 2_order : second order markov chain
                # mixed_order: mixed order markov chain (first and second order)
            * rain_quant_model: the model of daily rain quantity
                # weibull: weibull distribution (default value)
                # exponential: exponetial distribution
                # gamma: gamma distribution
                # hyperexp: hyperexponential distribution
        
        Returns
        -------
        an array of daily precipitation, each row represent the instance of continuous daily data for month. 

        """
        if not self.model_fitted: 
            print("Error: The weather generator model should be fitted before using it")
            return None
        if nb_real == 0: 
            print("Error: Number of realization should be greater or equal to one")
            return None
        
        
        self.rain_occ_model = rain_occ_model
        self.rain_quantity_model = rain_quant_model
        std = datetime(year, month, 1)
        ste = std + relativedelta(months = 1) 
        nbj = (ste - std).days
        res_rain = np.zeros((nb_real, nbj)) #final result
        
        mo = month - 1
        #loading weather generator model parameter
        prob0 = self.M1 
        temp_M1 = self.M1[mo]
        temp_M2 = self.M2[mo]
        temp_prob0 = self.prob0[mo]
        
        temp_fite = self.fit_expon[mo]
        temp_gam = self.fit_gamma[mo]
        temp_fitw = self.fit_weibull[mo]
        temp_fith = self.fit_hyperexpon[mo]
        
        for j in np.arange(nb_real):
            rain_occ = np.zeros(nbj)
            rain_q = np.zeros(nbj)
            rain_occ[0] = 0 if random.uniform(0, 1) < temp_prob0 else 1
            #generate rain occurence
            if self.rain_occ_model == "1_order":
                for i in np.arange(1, nbj):
                    if not rain_occ[i-1]: 
                        rain_occ[i] = 0 if random.uniform(0, 1) < temp_M1[0] else 1
                    else: 
                        rain_occ[i] = 0 if random.uniform(0, 1) < temp_M1[1] else 1
            elif self.rain_occ_model == "2_order":
                if not rain_occ[0]: 
                    rain_occ[1] = 0 if random.uniform(0, 1) < temp_M1[0] else 1
                else: 
                    rain_occ[1] = 0 if random.uniform(0, 1) < temp_M1[1] else 1

                for i in np.arange(2, nbj): 
                    if not rain_occ[i-2]: #
                        if not rain_occ[i-1]: #dd
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[0] else 1
                        else: #dw
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[1] else 1
                    else: 
                        if not rain_occ[i-1]: #wd
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[2] else 1
                        else: #ww
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[3] else 1
            else: #mixed order
                if not rain_occ[0]: 
                    rain_occ[1] = 0 if random.uniform(0, 1) < temp_M1[0] else 1
                else: 
                    rain_occ[1] = 0 if random.uniform(0, 1) < temp_M1[1] else 1
                for i in np.arange(2, nbj): 
                    if rain_occ[i-1]: 
                        rain_occ[i] = 0 if random.uniform(0, 1) < temp_M1[1] else 1
                    else: #
                        if not rain_occ[i-2]: #dd
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[0] else 1
                        else: #wd
                            rain_occ[i] = 0 if random.uniform(0, 1) < temp_M2[2] else 1
                            #generate rain model
            
            #generate rain quantity
            if self.rain_quantity_model == "weibull":
                for i in np.arange(nbj):
                    if rain_occ[i]: 
                        rain_q[i] = stats.weibull_min.rvs(c=temp_fitw[0], scale=temp_fitw[2])
            elif self.rain_quantity_model == "gamma":
                for i in np.arange(nbj):
                    if rain_occ[i]: 
                        rain_q[i] = stats.gamma.rvs(a=temp_gam[0], scale=temp_gam[2])
            elif self.rain_quantity_model == "exponential":
                for i in np.arange(nbj):
                    if rain_occ[i]: 
                        rain_q[i] = stats.weibull_min.rvs(c=temp_fite[0], scale=temp_fite[2])
            else:
                for i in np.arange(nbj):
                    if rain_occ[i]: 
                        rain_q[i] = hyper_d.rvs(p1=temp_fith[0] , beta1=temp_fith[1] , beta2=temp_fith[2])
            res_rain[j] = rain_q
        return res_rain