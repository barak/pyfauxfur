#!/usr/bin/env python
# encoding: utf-8
"""
Texture.py

Created by Olivier Le Floch on 2009-03-17.
Program written by Thomas Deniau and Olivier Le Floch.
Copyright (c) 2009. All rights reserved.

Portions of this code have been adapted from pygarrayimage :
  http://pypi.python.org/pypi/pygarrayimage/0.0.5
  http://code.astraw.com/projects/motmot/trac/browser/trunk/pygarrayimage

Please see the LICENSE file for this software and pygarrayimage's software
license.
"""

import unittest
import ctypes
from numpy import dstack, random, zeros
from pyglet.image import ImageData

class MorphogenesisImageData(ImageData):
  def __init__(self, width, height, D_s, D_a, D_b, beta_i):
    '''Initialize morphogenesis image data with specific calculation parameters

    :Parameters:
      `width` : int
        Width in pixels of the calculated image
      `height` : int
        Height in pixels of the calculated image
      `D_s` : float
      `D_a` : float
      `D_b` : float
      `beta_i` : float
    '''
    
    print 'Generating texture with the following parameters :'
    print '   Reaction rate =', D_s
    print 'A diffusion rate =', D_a
    print 'B diffusion rate =', D_b
    print '    B decay rate =', beta_i
    print ''
    print '   texture width =', width
    print '  texture height =', height
    print '...'
    
    self.width  = width
    self.height = height
    
    self.grid_a = random.rand(width, height)
    self.grid_b = random.rand(width, height)
    
    self.data_ptr = ctypes.c_void_p()
    self.make_texture()
    
    # TODO : Do we need to specify the 'pitch' keyword parameter ?
    super(MorphogenesisImageData, self).__init__(
      width, height, 'RGB', None)
    
    self.D_s    = D_s
    self.D_a    = D_a
    self.D_b    = D_b
    self.beta_i = beta_i
    
    self.dx2     = 1.0 / width**2
    self.dy2     = 1.0 / height**2
    self.dnr_inv = 0.5 / (self.dx2 + self.dy2)
    
    self.iteration = 0
  
  def _convert(self, format, pitch):
    if format == self._current_format and pitch == self._current_pitch:
      return self.data_ptr
    else:
      raise ValueError('Unable to retrieve the texture data without converting.')
  
  def make_texture(self):
    '''
    Calculates the colors for each point in the grid, and then copies this
    data into the image.
    '''
    grid = (255 * dstack((self.grid_a, zeros((self.width, self.height), 'd'), self.grid_b))).astype('u1')
    array_interface = grid.__array_interface__
    
    data_ptr_int, readonly = array_interface['data']
    self.data_ptr.value = data_ptr_int
    
    # Maintain references so they're not deallacoted
    self.grid_retainer            = grid
    self.array_interface_retainer = array_interface
  
  def dirty(self):
    '''
    Force an update of the texture data.
    '''

    texture = self.texture
    internalformat = None
    self.blit_to_texture(
      texture.target, texture.level, 0, 0, 0, internalformat)
  
  def step(self):
    dx2     = self.dx2
    dy2     = self.dy2
    dnr_inv = self.dnr_inv
    
    height = self.height
    width  = self.width
    
    A_o = self.grid_a
    A_n = zeros((width, height), 'd')
    B_o = self.grid_b
    B_n = zeros((width, height), 'd')
    
    print 'Start iteration', self.iteration
    
    for i in range(0, width):
      # Treat the surface as a torus by wrapping at the edges
      iplus1  = i + 1 if i < width - 1 else 0
      iminus1 = i - 1 if i > 0 else width - 1
      
      for j in range(0, height):
        jplus1  = j + 1 if j < height -1 else 0
        jminus1 = j - 1 if j > width - 1 else height -1

        # Component A
        A_diffuse  = self.D_a * (A_o[iplus1][j] - 2.0 * A_o[i][j] + A_o[iminus1][j] + A_o[i][jplus1] - 2.0 * A_o[i][j] + A_o[i][jminus1])
        A_reaction = A_o[i][j] * B_o[i][j] - A_o[i][j] - 12.0
        
        A_n[i][j] = A_o[i][j] + 0.01 * (A_reaction + A_diffuse)
        
        if A_n[i][j] < 0.0:
          A_n[i][j] = 0.0

        # Component B
        B_diffusion = self.D_b * (B_o[iplus1][j] - 2.0 * B_o[i][j] + B_o[iminus1][j] + B_o[i][jplus1] - 2.0 * B_o[i][j] + B_o[i][jminus1])
        B_reaction  = 16.0 - A_o[i][j] * B_o[i][j]
        B_n[i][j]   = B_o[i][j] + 0.01 * (B_reaction + B_diffusion)
        
        if B_n[i][j] < 0.0:
          B_n[i][j] = 0.0
    
    self.grid_a = A_n
    self.grid_b = B_n
    
    print 'End iteration', self.iteration
    
    self.iteration += 1
  
  def __repr__(self):
    return str((self.grid_a, self.grid_b))

class TextureTests(unittest.TestCase):
  def setUp(self):
    pass

if __name__ == '__main__':
  unittest.main()
