import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod
from shad_prog import *
from vbo import * 

# Define an abstract interface for Vertex Array Objects (VAOs)
class VAO_interface(ABC):

    # Define an abstract method for getting a VAO
    @abstractmethod
    def g_vao(self):
        raise NotImplementedError
    
    # Define an abstract method for destroying a VAO
    @abstractmethod
    def destroy(self):
        raise NotImplementedError
    

class general_VAO():

    def __init__(self,app):
        self.app = app
        self.sp = shader_program(self.app)
        self.vbo = general_VBO(self.app)
        self.fog = True if input('Use fog (y/n)? ') == 'y' else False 
        self.fursp = self.sp.obj['furmark']
        self.new_sp = self.sp.obj['default'] if not self.fog else self.sp.obj['fog_default']
        self.new_sbsp = self.sp.obj['skybox'] if not self.fog else self.sp.obj['fog_skybox']
        self.vao_arr = {
            'cube' : self.g_vao(self.sp.obj['default'] if not self.fog else self.sp.obj['fog_default'],self.vbo.vbo_d['cube'].g_vbo(),'2f 3f 3f',['in_txcoord','in_norm','in_position']),
            'skybox' : self.g_vao(self.sp.obj['skybox'] if not self.fog else self.sp.obj['fog_skybox'],self.vbo.vbo_d['skybox'].g_vbo(),'3f',['in_position']),
            'twins' : self.g_vao(self.sp.obj['default'] if not self.fog else self.sp.obj['fog_default'],self.vbo.vbo_d['twins'].g_vbo(),'2f 3f 3f',['in_txcoord','in_norm','in_position']),
        }

    def g_vao(self,sp,vbo,format,attrs):
        # Define a VAO with a single buffer containing 3 vectors with floating point values
        return self.app.ctx.vertex_array(sp, [(vbo, format, *attrs)], skip_errors=True)

    def destroy(self):
        self.sp.destroy()

