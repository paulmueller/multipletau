# -*- coding: utf-8 -*-
""" Multiple Tau Algorithms
    
    Author: Paul Müller
"""

from __future__ import division
from __future__ import print_function

import numpy as np

from _multipletau import *

from matplotlib import pylab as plt

def GenerateExpNoise(N, taud=20., variance=1., deltat=1.):
    # length of mean0 trace
    N_steps = N
    dt = int(deltat)
    # time trace
    t = np.arange(N_steps)
    # AR-1 processes - what does that mean?
    # time constant (inverse of correlationtime taud)
    g = 1./taud
    # variance
    s0 = variance
    
    # normalization factor (memory of the trace)
    exp_g = np.exp(-g*dt)
    one_exp_g = 1-exp_g
    z_norm_factor = np.sqrt(1-np.exp(-2*g*dt))/one_exp_g
    
    # create random number array
    # generates random numbers in interval [0,1)
    randarray = np.random.random(N_steps)
    # make numbers random in interval [-1,1)
    randarray = 2*(randarray-0.5)
    
    # simulate exponential random behavior
    z = np.zeros(N_steps)
    z[0] = one_exp_g*randarray[0]
    for i in np.arange(N_steps-1)+1:
        z[i] = exp_g*z[i-1] + one_exp_g*randarray[i]
        
    z = z * z_norm_factor*s0
    return z, t


# Edit parameters
N = 278000
countrate = 250. # in kHz
taudiff = 55. # in us
deltat = 2e-6 # time discretization [s]

print("Generating exponentially correlated noise.")
# Do not edit
taudiff *= 1e-6/deltat
data, times = GenerateExpNoise(N, taud=taudiff, deltat=1.)
countrate *= deltat*1000 # since we want kHz instead of Hz
# We set one bin to 1e-6 s.
print("Performing autocorrelation.")
G = ac_bin(np.float32(data+countrate), deltat=deltat) 

# Calculate the expected curve
x = G[:,0]
y = 1.35*np.exp(-x/taudiff/deltat)

print("Plotting.")
fig = plt.figure()
ax = fig.add_subplot(2,1,1)
ax.set_xscale('log')
plt.plot(x, G[:,1] -1)
plt.plot(x, y)
plt.show()