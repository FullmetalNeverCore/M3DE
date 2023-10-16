import numpy as np 
from components.vao import * 
from components.vbo import *
from components.shad_prog import *
import pywavefront
from abc import ABC, abstractmethod
from components.txuring import *
import copy
import datetime 
import moderngl as mgl
import pygame
import moderngl_window as mglw
import time
from components.cam import *
import math 
from numba import njit



class Chunk:
    def __init__(self,app)->None:
        self.app = app 
        self.chunk_size = 32
        self.half_chunk = self.chunk_size // 2
        self.chunk_area = self.chunk_size * self.chunk_size
        self.chunk_vol = self.chunk_area * self.chunk_size
        self.b_voxel = self.b_vox()
    
    def b_vox(self)->np.array:
        vox = np.zeros(self.chunk_vol,dtype='uint8')
        for x in range(self.chunk_size):
            for z in range(self.chunk_size):
                for y in range(self.chunk_size): 
                    vox[x+self.chunk_size*z+self.chunk_area*y] = x+y+z
        return vox

