# -*- coding: utf-8 -*-
"""
@author: Nieves Montes Gómez

@date: 19/01/2020
  
@description: Implementation of Simulated Annealing algorithm to solve the lizards
problem (analogous to 8-queens).
"""

import configuration
import coolingSchedule
import os
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 32})


"""Parameters related to the SA algorithm"""
Lmax = 100 # maximum number of total outer loop iterations
Lamax = 10 # maximum number of accepted inner loop iterations
HTsw = 0.99 # minumum acceptance rate at starting temperature
Tini = 1.00 # initial temperature
dt = 0.01 # temperature increment to find starting temperature
kB = 1.0E-2 # Boltzmann constant

"""Parameters related to cooling schedule."""
alpha = 0.95 # geometric cooling
c = 0.30 # logarithmic cooling
deltaT = 0.01 # linear cooling


def NewConfiguration(config):
  """Takes in a configuration, and returns a new configuration created by 
  moving an attacked lizard to a new available position."""
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
  """Takes in a configuration and, for a fixed temperature, it looks for new
  configurations until either of this conditions is fulfilled:
    - The loop has exceeded a maximum number of iterations Lmax.
    - The loop has accepted a maximum number of new configurations Lamax.
    - The loop has found a new configuration with 0 energy, a solution to the problem.
  The function returns the last accepted configuration and the rate of accepted
  configurations."""
  if not isinstance(config, configuration.Configuration):
    raise ValueError('Argument is not a configuration.')
  L = 0 # total iterations
  La = 0 # total accepted iterations
  while (L < Lmax) and (La < Lamax) and (config.energy > 0):
    newConfig = NewConfiguration(config)
    if (newConfig.energy < config.energy):
      config = copy.deepcopy(newConfig)
      La += 1
    else:
      acceptProb = float(os.urandom(1)[0]/255)
      if acceptProb < math.exp((config.energy - newConfig.energy)/(kB*temp)):
        config = copy.deepcopy(newConfig)
        La += 1
    L += 1
  return (config, La/Lamax)


def SimulatedAnnealing(treeList = [], cooling='geometric'):
  """Provided a treeList in the board, use Simulated Annealing to find a
  configuration of the lizards such that any of them is in danger.
  Start by creating an initial configuration with random lizard positions.
  The tree positions is taken from input. The cooling argument specifies the
  cooling schedule (geometric by default). The algorithm is only allowed to 
  halt once a solution has been found or the outer loop has exceeded a maximum
  number of iterations."""
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
  while (candidate.energy > 0) and (outerIter <= Lmax):
    candidate = InnerLoop(candidate, temp)[0]
    print('Iteration ' + str(outerIter))
    print('Temperature: ' + str(temp))
    print('Lizards under attack: ' + str(candidate.energy))
    print('\n')
    iterList.append(outerIter)
    lizUnderAttack.append(candidate.energy)
    tempList.append(temp)
    # update temperature according to schedule
    if cooling == 'geometric':
      temp = coolingSchedule.geometric(temp, alpha)
    elif cooling == 'logarithmic':
      temp = coolingSchedule.logarithmic(c, outerIter)
    elif cooling == 'linear':
      temp = coolingSchedule.linear(temp, deltaT)
    else:
      raise ValueError('Invalid cooling schedule.')
    outerIter += 1
  print('A solution has been found after ' + str(outerIter-1) + ' iterations.')
  
  # roll back last temperature change
  if cooling == 'geometric':
      temp = temp/alpha
  elif cooling == 'logarithmic':
    if outerIter == 1:
      outerIter += 1
    temp = c / math.log(outerIter-1)
  elif cooling == 'linear':
    temp += deltaT
  else:
    raise ValueError('Invalid cooling schedule.')
    
  print('Final temperature: ' + str(temp) + '\n')
  return (candidate, iterList, lizUnderAttack, tempList, outerIter)
  
#%%
"""Execute following lines to get the solution for configurations with different
number of trees."""
treeList0 = []
treeList1 = [(4,4)]
treeList2 = [(3,4), (5,5)]
treeList3 = [(1,1), (4,6), (5,3)]

# tweak treeList argument to try a different tree setup
solution = SimulatedAnnealing(treeList = treeList0, cooling = 'logarithmic')
solconfig = solution[0]
solconfig.plot()
iterList = solution[1]
lizUnderAttack = solution[2]
tempList = solution[3]
coolingSchedule.plotResults(iterList, lizUnderAttack, tempList)
#%%


#%%
"""Find the average number of outer loops iterations necessary for many configurations."""
N = 100
listOfTreeLists = [treeList0]#, treeList1, treeList2, treeList3]

for setup in listOfTreeLists:
  s = 0.
  for _ in range(N):
    solution = SimulatedAnnealing(treeList = setup, cooling = 'logarithmic')
    s += solution[4]
  avg = s/N
  print('\nConfiguration ' + str(listOfTreeLists.index(setup)) + ': average iterations: ' + str(avg) + '\n') 
#%%