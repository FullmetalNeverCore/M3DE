import numpy as np
import moderngl as mgl
import pywavefront
import glm
from abc import ABC, abstractmethod

# Define an abstract base class for the shader program interface
class shader_program_interface(ABC):


    @abstractmethod
    def destroy(self):
        raise NotImplementedError
    

    @abstractmethod
    def g_shader_file(self):
        raise NotImplementedError


class shader_program(shader_program_interface):
    
    # Initialize the shader program
    def __init__(self,app)->None:
        self.app = app  
        self.obj = {}
        self.obj['default'] = self.g_shader_file('default') # Get the default shader file
        self.obj['skybox'] = self.g_shader_file('skybox')   # Get the skybox shader file
        self.obj['fog_default'] = self.g_shader_file('fog_default') # Get the default shader file
        self.obj['fog_skybox'] = self.g_shader_file('fog_skybox')   # Get the skybox shader file
        self.obj['furmark'] = self.g_shader_file('furmark')
        self.obj['mine'] = self.g_shader_file('mine')
     
    # Destroy the shader program
    def destroy(self)->None:
        [p.release() for p in self.obj.values()] 
    
    # Get the shader file
    def g_shader_file(self,shader)->'Shader Program':
        print('reading shader_file...')
        with open(f'./shaders/{shader}.vert') as file:
            vert_shad = file.read()  
            file.close()   
        with open(f'./shaders/{shader}.frag') as file:
            frag_shad = file.read()  
            file.close()    
        return self.app.ctx.program(vertex_shader=vert_shad,fragment_shader=frag_shad)  # Return the program