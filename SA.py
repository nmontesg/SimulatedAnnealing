# -*- coding: utf-8 -*-
"""
@author: Nieves Montes Gómez

@date: 19/01/2020
  
@description: Implementation of Simulated Annealing algorithm to solve the lizards
problem (analogous to 8-queens).
"""

import configuration
import os
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})

"""Variables related to the SA algorithm:
    Lmax: maximum number of total inner loop iterations.
    Lamax: maximum number of accepted inner loop iterations.
    LTsw: minumum acceptance rate of new iterations.
    zerot: minumum temperature.
    HTsw: minumum acceptance rate at starting temperature.
    Tini: initial temperature.
    dt: temperature increment to find starting temperature.
    alpha: exponential decay rate of temperature."""
Lmax = 100
Lamax = 10
HTsw = 0.99
Tini = 1.0
dt = 0.1
alpha = 0.95


def NewConfiguration(config):
  """Returns a new configuration created by moving an attacked lizard
  to a new available position."""
  if not isinstance(config, configuration.Configuration):
    raise ValueError('Argument is not a configuration.')
  newConfig = copy.deepcopy(config)
  attackedArray = np.asarray(newConfig.attacked, dtype = np.bool8)
  attackedLizards = np.where(attackedArray == True)[0]
  if attackedLizards.size == 0:
    return newConfig
  randomIndex = int(os.urandom(1)[0]/255*attackedLizards.size - 1.E-9)
  movableLizard = attackedLizards[randomIndex]
  newPosition = (int(os.urandom(1)[0]/255*8 - 1.E-9),
                 int(os.urandom(1)[0]/255*8 - 1.E-9))
  while (newPosition in newConfig.lizardPositions) or (newPosition in newConfig.treePositions):
    newPosition = (int(os.urandom(1)[0]/255*8 - 1.E-9),
                   int(os.urandom(1)[0]/255*8 - 1.E-9))
  newConfig.lizardPositions[movableLizard] = newPosition
  newConfig.findAttackedLizardsAndEnergy()
  return newConfig


def InnerLoop(config, temp):
  if not isinstance(config, configuration.Configuration):
    raise ValueError('Argument is not a configuration.')
  if config.energy == 0:
    return
  L = 0 # total iterations
  La = 0 # total accepted iterations
  while (L < Lmax) and (La < Lamax):
    newConfig = NewConfiguration(config)
    if (newConfig.energy < config.energy):
      config = copy.deepcopy(newConfig)
      La += 1
      print
    else:
      acceptProb = float(os.urandom(1)[0]/255)
      if acceptProb < math.exp((config.energy - newConfig.energy)/temp):
        config = copy.deepcopy(newConfig)
        La += 1
    L += 1
  return (config, La/Lamax)


def plotResults(iterList, lizUnderAttack, tempList):
  fig, ax1 = plt.subplots(figsize=(10,10))
  
  color = 'tab:blue'
  ax1.set_xlabel('Outer loop iteration')
  ax1.set_ylabel('Lizards under attack', color=color)
  ax1.plot(iterList, lizUnderAttack, linestyle = '-', linewidth = 2.5,
           marker = 'o', markersize = 8, color=color)
  ax1.tick_params(axis='y', labelcolor=color)
  plt.grid()
  
  ax2 = ax1.twinx()
  color = 'tab:red'
  ax2.set_ylabel('Temperature', color=color)
  ax2.plot(iterList, tempList, linestyle = '-', linewidth = 2.5,
           marker = 'o', markersize = 8, color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  plt.show()


def SimulatedAnnealing(treeList = []):
  """Provided a treeList in the board, use Simulated Annealing to find a
  configuration of the lizards such that any of them is in danger."""
  if not isinstance(treeList, list):
    raise ValueError('Argument treeList is not a list.')
  initialConf = configuration.Configuration(treeList = treeList)
  initialConf.randomLizards()
  initialConf.findAttackedLizardsAndEnergy()
  
  # Find starting temperature
  temp = Tini
  r = InnerLoop(initialConf, temp)[1]
  while (r < HTsw):
    temp += dt
    r = InnerLoop(initialConf, temp)[1]
  print('Initial temperature: ' + str(temp))
  print('Lizards under attack: ' + str(initialConf.energy) + '\n')
    
  # SA - outer loop
  iterList = [0]
  lizUnderAttack = [initialConf.energy]
  tempList = [temp]
  candidate = initialConf
  outerIter = 1
  while (candidate.energy > 0):
    (candidate, r) = InnerLoop(candidate, temp)
    print('Iteration ' + str(outerIter))
    print('Temperature: ' + str(temp))
    print('Lizards under attack: ' + str(candidate.energy))
    print('\n')
    iterList.append(outerIter)
    lizUnderAttack.append(candidate.energy)
    tempList.append(temp)
    temp *= alpha
    outerIter += 1
  plotResults(iterList, lizUnderAttack, tempList) 
  return candidate
  

"""Execute following lines to get the solution for configuration 1 (no trees)."""
solutionA = SimulatedAnnealing()
print(solutionA)
    
"""Execute following lines to get the solution for configuration 2 (two trees).
CAUTION: change name of plot file generated when executing line ???."""
solutionB = SimulatedAnnealing(treeList=[(3,4), (5,5)])
print(solutionB)
