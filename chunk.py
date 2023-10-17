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
from components.chunk_config import *
from components.mesh import *
from components.building_ops import *



class Chunk:
    def __init__(self,app,pos=(0,0,0),sp=None,vao=None)->None:
        self.app = app 
        self.pos = pos
        self.sp = sp
        self.vao = vao
        self.empty_spc = True
        self.mesh = None 
    
    def b_vox(self)->np.array:
        vox = np.zeros(chunk_vol,dtype='uint8')
        zx,zy,zz = glm.ivec3(self.pos) * chunk_size
        gen_terr(vox,zx,zy,zz)
        if np.any(vox):
            self.empty_spc = False
        return vox
    
    def get_model_m(self):
        return glm.translate(glm.mat4(),glm.vec3(self.pos)*chunk_size)

    def b_mesh(self):
        self.mesh = Mesh(chunk=self) 
    
    def render(self):
        if not self.empty_spc:
            self.sp['model_mat'].write(self.get_model_m())
            self.mesh.render()