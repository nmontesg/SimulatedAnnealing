# -*- coding: utf-8 -*-
"""
@author: Nieves Montes Gómez

@date: 19/01/2020
  
@description: module for Configuration class, that represents a possible 
configuration of lizards in a 8x8 board.
"""

import os

class Configuration(object):
  """Class that represents a candidate configuration. Attributes are:
    - List of lizard positions.
    - List of trees positions.
    - Energy of the configuration, as in number of attacks."""
  def __init__(self, treeList=[]):
    self.lizardPositions = []    
    if isinstance(treeList, list):
      self.treePositions = treeList
    else:
      self.treePositions = []
    self.attacked = [False for _ in range(8)]
    self.energy = 0
  
  
  def randomLizards(self):
    """Choose 8 different random positions for lizards."""
    i = 0
    while(i<8):
      newLizard = (int(os.urandom(1)[0]/255*8 - 1.E-9),
                   int(os.urandom(1)[0]/255*8 - 1.E-9))
      if (newLizard not in self.lizardPositions) and (newLizard not in self.treePositions):
        self.lizardPositions.append(newLizard)
        i += 1
        
  def isLizardAttacked(self, l):
    """Find out if l-th lizard is under attack."""
    i = self.lizardPositions[l][0] # row of lizard
    j = self.lizardPositions[l][1] # column of lizard
    
    # scan row to the left
    colInd = j-1
    while colInd >= 0:
      if (i,colInd) in self.lizardPositions:
        return True
      elif (i,colInd) in self.treePositions:
        break
      else:
        colInd -= 1
    # scan row to the right
    colInd = j+1
    while colInd < 8:
      if (i,colInd) in self.lizardPositions:
        return True
      elif (i,colInd) in self.treePositions:
        break
      else:
        colInd += 1
    
    # scan column upwards
    rowInd = i-1
    while rowInd >= 0:
      if (rowInd,j) in self.lizardPositions:
        return True
      elif (rowInd,j) in self.treePositions:
        break
      else:
        rowInd -= 1
    # scan column downwards
    rowInd = i+1
    while rowInd < 8:
      if (rowInd,j) in self.lizardPositions:
        return True
      elif (rowInd,j) in self.treePositions:
        break
      else:
        rowInd += 1
        
    # scan positive diagonal to the NE
    rowInd = i-1
    colInd = j+1
    while (rowInd >= 0) and (colInd < 8):
      if (rowInd,colInd) in self.lizardPositions:
        return True
      elif (rowInd,colInd) in self.treePositions:
        break
      else:
        rowInd -= 1
        colInd += 1
    # scan positive diagonal to the SW
    rowInd = i+1
    colInd = j-1
    while (rowInd < 8) and (colInd >= 0):
      if (rowInd,colInd) in self.lizardPositions:
        return True
      elif (rowInd,colInd) in self.treePositions:
        break
      else:
        rowInd += 1
        colInd -= 1
        
    # scan negative diagonal to the NW
    rowInd = i-1
    colInd = j-1
    while (rowInd >= 0) and (colInd >= 0):
      if (rowInd,colInd) in self.lizardPositions:
        return True
      elif (rowInd,colInd) in self.treePositions:
        break
      else:
        rowInd -= 1
        colInd -= 1
    # scan negative diagonal to the SE
    rowInd = i+1
    colInd = j+1
    while (rowInd < 8) and (colInd < 8):
      if (rowInd,colInd) in self.lizardPositions:
        return True
      elif (rowInd,colInd) in self.treePositions:
        break
      else:
        rowInd += 1
        colInd += 1  
        
    return False
    
  
  def findAttackedLizardsAndEnergy(self):
    """Find which lizards are attacked and compute energy of the configuration
    as the number of attacked lizards."""
    for i in range(8):
      self.attacked[i] = self.isLizardAttacked(i)
    self.energy = self.attacked.count(True)
  
  
  def __str__(self):
    output = ' _______________________________________________\n'
    
    for i in range(8):
      output += '|     |     |     |     |     |     |     |     |\n'
      output += '|'
      for j in range(8):
        if (i,j) in self.lizardPositions:
          cell = 'L'
        elif (i,j) in self.treePositions:
          cell = 'T'
        else:
          cell = ' '
        output += '  ' + cell + '  |'
      output += '\n|_____|_____|_____|_____|_____|_____|_____|_____|\n'
      
    return output
  