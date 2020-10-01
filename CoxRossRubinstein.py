# Cox-Ross-Rubinstein for Eurpean and American style options

#Code is straightforward and only numpy is required


import numpy as np

#S        -> Spot price of the underlying
#K        -> Strike price for the option
#sigma    -> Annualized volatility of the underlying
#r        -> continously compounded risk-free rate
#T        -> option's time to expiration in years
#steps    -> number of steps to be calculated in the tree
#q        -> continously compounded dividend yield (default is 0)
#call     -> specify put or call option (default is call)
#american -> specify if early exercise (default is true, false for European style)


def crr(S,K,sigma,r,T,steps,q=0,call=True,american=True): 
    # Assigning paramter values
    dt=T/steps
    u=np.exp(dt**0.5 *sigma)
    d=np.exp(-(dt**0.5 *sigma))
    p=(np.exp((r-q)*dt)-d)/(u-d)
    
    #Pre-allocating the underlying's price array
    pricetree=np.zeros([steps+1,steps+1],dtype='float64')
    pricetree[0,0]=S
    
    #The tree is calculated for the underlying's price
    for i in range(1,steps+1):
       pricetree[:i,i]=pricetree[:i,i-1]*u
       pricetree[i,i]=pricetree[i-1,i-1]*d
       
    #Tree for the option value
    optiontree=np.zeros([steps+1,steps+1],dtype='float64')
    if call:
        optiontree[:,steps]=np.maximum(pricetree[:,-1 ]-K,0)
    else:
         optiontree[:,steps]=np.maximum(K-pricetree[:,-1 ],0)
    
    for i in range(steps-1,-1,-1):
        optiontree[:i+1,i]=np.exp(-(r*dt))*(optiontree[:i+1,i+1]*p+\
                                            (1-p)*optiontree[1:i+2:1,i+1])
        #Early exercise    
        if american :
            if call :
                optiontree[:i+1,i]=np.maximum( pricetree[:i+1,i]-K, \
                                       optiontree[:i+1,i])
            else:
                optiontree[:i+1,i]=np.maximum(K-pricetree[:i+1,i], \
                                              optiontree[:i+1,i])
                    
    #Finally, the function outputs the option value, and the price and 
    # option value trees.              
    return optiontree[0,0], pricetree, optiontree
    


                                        
##### Using the function with some given parameters ######
    
S=50;
K=30;
sigma= 0.3;
r=0.05;
T=1;
steps=200;


price,pricearray,optionarray=crr(S,K,sigma,r,T,steps)


    
