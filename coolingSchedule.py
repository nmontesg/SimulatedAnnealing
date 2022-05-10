# -*- coding: utf-8 -*-
"""
@author: Nieves Montes Gómez

@date: 19/01/2020

@description: Cooling schedule functions and auxiliary plotting function.
"""

import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


"""Cooling schedule functions."""
def logarithmic(c, k):
  return c/math.log(1+k)

def geometric(temp, alpha):
  return temp*alpha

def linear(temp, delta):
  newTemp = temp - delta
  if newTemp > 0:
    return newTemp
  else:
    return 1.0E-12



def plotResults(iterList, lizardsUnderAttack, tempList):
  """Plot the evolution of energy and temperature as a function of outer loop
  iteration number."""
  fig, ax1 = plt.subplots(figsize=(10,10))
  
  color = 'tab:blue'
  ax1.set_xlabel('Outer loop iteration')
  ax1.set_ylabel('Lizards under attack', color=color)
  ax1.plot(iterList, lizardsUnderAttack, linestyle = '-', linewidth = 2.5,
           marker = 'o', markersize = 8, color=color)
  ax1.tick_params(axis='y', labelcolor=color)
  ax1.xaxis.set_major_locator(MaxNLocator(integer=True))
  plt.grid()
  
  ax2 = ax1.twinx()
  color = 'tab:red'
  ax2.set_ylabel('Temperature', color=color)
  ax2.plot(iterList, tempList, linestyle = '-', linewidth = 2.5,
           marker = 'o', markersize = 8, color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  plt.show()