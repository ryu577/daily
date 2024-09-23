import numpy as np


a = 600000
t = 360
r = 3.25/100/12
u = a*r/(1-(1+r)**-t)


# After some additional payments, the loan amount has gone down.
a = 580000
r = 3.25/100/12
t = np.log(u/(u-a*r))/np.log(1+r)
print(t)


a = 600000
r = 3.25/100/12
t = 360
x = 2
t1 = t*np.log(1+r)/np.log(1+r/x)
print(t1)

