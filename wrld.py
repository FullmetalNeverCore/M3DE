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
from components.perlin import *
from components.raycast import *
from components.chunk import *
from components.chunk_config import *

class World:
    def __init__(self,app,sp=None,vao=None):
        self.app = app 
        self.sp = sp
        self.vao = vao
        self.ch = [None for x in range(world_v)]
        self.voxel = np.empty([world_v,chunk_vol],dtype='uint8')
        self.build_chunk()
        self.build_mesh()
    

    def build_chunk(self):
        for x in range(world_wid):
            for y in range(world_hei):
                for z in range(world_dim):
                    chunk = Chunk(app=self.app,pos=(x,y,z),sp=self.sp,vao=self.vao,wrld=self)
                    ch_ind = x + world_wid * z + world_area * y
                    self.ch[ch_ind] = chunk 
                    self.voxel[ch_ind] = chunk.b_vox()
                    chunk.b_voxel = self.voxel[ch_ind]
    

        
    def build_mesh(self):
        for x in self.ch:
            x.b_mesh()
    
    def render(self):
        for x in self.ch:
            x.render()