# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 22:12:41 2020

@author: mnm24
"""

import numpy as np
import os
from scipy.special import comb

class Configuration(object):
  def __init__(self, treeList=[]):
    self.board = np.zeros(shape=(8,8), dtype=np.uint8)
    if isinstance(treeList, list):
      for position in treeList:
        self.board[position[0]-1,position[1]-1] = 2
    self.energy = 0
  
  def randomLizards(self):
    i = 0
    while(i<8):
      newLizard = [int(os.urandom(1)[0]/255*7),
                   int(os.urandom(1)[0]/255*7)]
      if self.board[newLizard[0],newLizard[1]] == 0:
        self.board[newLizard[0],newLizard[1]] = 1
        i += 1
        
  def findEnergy(self): # !!!! falta contar els atacs en diagonal
    # scan rows:
    for i in range(8):
      lizardsInRow = 0
      lizardsInCol = 0
      for j in range(8):
        # deal with rows
        if self.board[i][j] == 1:
          lizardsInRow += 1
        if self.board[i][j] == 2:
          if lizardsInRow > 1:
            self.energy += int(comb(lizardsInRow, 2, exact=True))
          lizardsInRow = 0
        # deal with columns
        if self.board[j][i] == 1:
          lizardsInCol += 1
        if self.board[j][i] == 2:
          if lizardsInCol > 1:
            self.energy += int(comb(lizardsInCol, 2, exact=True))
          lizardsInCol = 0
          
      if lizardsInRow > 1:
        self.energy += int(comb(lizardsInRow, 2, exact=True))
      if lizardsInCol > 1:
        self.energy += int(comb(lizardsInCol, 2, exact=True))
    # scan diagonals:
  
  def __str__(self):
    output = ' _______________________________________________\n'
    for i in range(8):
      output += '|     |     |     |     |     |     |     |     |\n'
      output += '|'
      for j in range(8):
        if self.board[i][j] == 0:
          cell = ' '
        elif self.board[i][j] == 1:
          cell = 'L'
        elif self.board[i][j] == 2:
          cell = 'T'
        output += '  ' + cell + '  |'
      output += '\n|_____|_____|_____|_____|_____|_____|_____|_____|\n'
      
    return output
      

problemA = Configuration()
problemB = Configuration(treeList = [(4,5), (6,6)])
problemA.randomLizards()
problemB.randomLizards()
print(problemB)
problemB.findEnergy()
print(problemB.energy)