import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod



class VAO_interface(ABC):
    

    @abstractmethod
    def g_vao(self):
        raise NotImplementedError
    
    @abstractmethod
    def destroy(self):
        raise NotImplementedError
    
class tri_VAO(VAO_interface):

    def __init__(self,app):
        self.app = app
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        #vao - vertex array obj
        vao = self.app.ctx.vertex_array(self.app.shader_prog,[(self.app.vbo,'3f','in_position')])
        return vao #3f buffer format - buffer with 3 vectors with floating point values
    
class cube_VAO(VAO_interface):
    def __init__(self,app):
        self.app = app
        self.format = '2f 3f 3f'
        self.attrs = ['in_txcoord','in_norm','in_position']
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        #vao - vertex array obj
        vao = self.app.ctx.vertex_array(self.app.shader_prog,
                                        [(self.app.vbo,self.format,*self.attrs)])
        return vao 
    
class twins_VAO(VAO_interface):
    def __init__(self,app):
        self.app = app
        self.format = '2f 3f 3f'
        self.attrs = ['in_txcoord','in_norm','in_position']
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        #vao - vertex array obj
        vao = self.app.ctx.vertex_array(self.app.shader_prog,
                                        [(self.app.vbo,self.format,*self.attrs)])
        return vao 