import numpy as np
import moderngl as mgl
import pywavefront
import glm
from abc import ABC, abstractmethod

# Define an abstract base class for the shader program interface
class shader_program_interface(ABC):

    # Define an abstract method for destroying the shader program
    @abstractmethod
    def destroy(self):
        raise NotImplementedError
    
    # Define an abstract method for getting the shader file
    @abstractmethod
    def g_shader_file(self):
        raise NotImplementedError

# Define a concrete implementation of the shader program interface
class shader_program(shader_program_interface):
    
    # Initialize the shader program
    def __init__(self,app):
        self.app = app  
        self.obj = {}
        self.obj['default'] = self.g_shader_file('default') # Get the default shader file
        self.obj['skybox'] = self.g_shader_file('skybox')   # Get the skybox shader file
        self.obj['fog_default'] = self.g_shader_file('fog_default') # Get the default shader file
        self.obj['fog_skybox'] = self.g_shader_file('fog_skybox')   # Get the skybox shader file
        self.obj['furmark'] = self.g_shader_file('furmark')
     
    # Destroy the shader program
    def destroy(self):
        [p.release() for p in self.obj.values()] 
    
    # Get the shader file
    def g_shader_file(self,shader):
        print('reading shader_file...')
        with open(f'./shaders/{shader}.vert') as file:
            vert_shad = file.read()       # Read the vertex shader
        with open(f'./shaders/{shader}.frag') as file:
            frag_shad = file.read()       # Read the fragment shader
        return self.app.ctx.program(vertex_shader=vert_shad,fragment_shader=frag_shad)  # Return the program