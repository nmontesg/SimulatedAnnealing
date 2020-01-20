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
plt.rcParams.update({'font.size': 22})

"""Variables related to the SA algorithm:
    Lmax: maximum number of total inner loop iterations.
    Lamax: maximum number of accepted inner loop iterations.
    LTsw: minumum acceptance rate of new iterations.
    HTsw: minumum acceptance rate at starting temperature.
    Tini: initial temperature.
    dt: temperature increment to find starting temperature.
    kB: Boltzmann constant."""
Lmax = 100
Lamax = 10
HTsw = 0.99
Tini = 1.00
dt = 0.01
kB = 1.0E-5

"""Variables related to cooling schedule."""
alpha = 0.95 # geometric cooling
c = 0.3 # logarithmic cooling
deltaT = 0.005 # linear cooling


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
      if acceptProb < math.exp((config.energy - newConfig.energy)/(kB*temp)):
        config = copy.deepcopy(newConfig)
        La += 1
    L += 1
  return (config, La/Lamax)


def SimulatedAnnealing(treeList = [], cooling='geometric'):
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
    candidate = InnerLoop(candidate, temp)[0]
    print('Iteration ' + str(outerIter))
    print('Temperature: ' + str(temp))
    print('Lizards under attack: ' + str(candidate.energy))
    print('\n')
    iterList.append(outerIter)
    lizUnderAttack.append(candidate.energy)
    tempList.append(temp)
    # update according to schedule
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
    temp = c / math.log()
  elif cooling == 'linear':
    temp += deltaT
  else:
    raise ValueError('Invalid cooling schedule.')
  print('Final temperature: ' + str(temp))
  return (candidate, iterList, lizUnderAttack, tempList)
  

"""Execute following lines to get the solution for configuration A (no trees), 
or B (include treeList)."""
treeList = [(3,4), (5,5)]
solution = SimulatedAnnealing(cooling = 'geometric')
solconfig = solution[0]
solconfig.plot()
iterList = solution[1]
lizUnderAttack = solution[2]
tempList = solution[3]
coolingSchedule.plotResults(iterList, lizUnderAttack, tempList)
