import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod

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

# Define a concrete implementation of the VAO interface for a triangular VAO
class tri_VAO(VAO_interface):

    def __init__(self, app):
        self.app = app
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        # Define a VAO with a single buffer containing 3 vectors with floating point values
        vao = self.app.ctx.vertex_array(self.app.shader_prog,[(self.app.vbo,'3f','in_position')])
        return vao

# Define a concrete implementation of the VAO interface for a cuboid VAO
class cube_VAO(VAO_interface):

    def __init__(self, app):
        self.app = app
        self.format = '2f 3f 3f'
        self.attrs = ['in_txcoord','in_norm','in_position']
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        # Define a VAO with a buffer containing 2 vectors, 3 vectors, and 3 vectors with floating point values respectively
        vao = self.app.ctx.vertex_array(self.app.shader_prog, [(self.app.vbo, self.format, *self.attrs)])
        return vao 

# Define a concrete implementation of the VAO interface for a skybox VAO
class skybox_VAO(VAO_interface):

    def __init__(self, app):
        self.app = app
        self.format = '3f'
        self.attrs = ['in_position']
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        # Define a VAO with a single buffer containing 3 vectors with floating point values
        vao = self.app.ctx.vertex_array(self.app.shader_prog, [(self.app.vbo, self.format, *self.attrs)])
        return vao 

# Define a concrete implementation of the VAO interface for a twins VAO
class twins_VAO(VAO_interface):

    def __init__(self, app):
        self.app = app
        self.format = '2f 3f 3f'
        self.attrs = ['in_txcoord','in_norm','in_position']
        self.vao = self.g_vao()

    def destroy(self):
        self.vao.release()
    
    def g_vao(self):
        # Define a VAO with a buffer containing 2 vectors, 3 vectors, and 3 vectors with floating point values respectively
        vao = self.app.ctx.vertex_array(self.app.shader_prog, [(self.app.vbo, self.format, *self.attrs)])
        return vao
