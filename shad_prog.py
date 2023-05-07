import numpy as np
import moderngl as mgl
import pywavefront
import glm
from abc import ABC, abstractmethod


class shader_program_interface(ABC):


    @abstractmethod
    def destroy(self):
        raise NotImplementedError
    

    @abstractmethod
    def g_shader_file(self):
        raise NotImplementedError


class shader_program(shader_program_interface):
    
    def __init__(self,app):
        self.app = app  
        self.obj = {}
        self.shader_prog = self.g_shader_file('default')
        self.obj['default'] = self.shader_prog
        self.model_mat = self.get_model_m()
        self.on_init()
    
    #model matrix
    def get_model_m(self):
        model = glm.mat4()
        model = glm.translate(model,self.app.pos)
        return model 
    def update(self):
        # for moving the cube
        model_mat = glm.rotate(self.model_mat,self.app.app.time,glm.vec3(0,1,0))
        self.shader_prog['model_mat'].write(model_mat)
        self.shader_prog['v_proj'].write(self.app.app.cam.view_matrix)
        self.shader_prog['camP'].write(self.app.app.cam.position)

    def on_init(self):
        #bulb 
        self.shader_prog['bulb.pos'].write(self.app.app.bulb.pos)
        self.shader_prog['bulb.amb'].write(self.app.app.bulb.amb)
        self.shader_prog['bulb.spe'].write(self.app.app.bulb.spec)
        self.shader_prog['tx_s'] = 0
        self.app.tx.use() #  use texture
        self.shader_prog['m_proj'].write(self.app.app.cam.proj_matrix)
        self.shader_prog['v_proj'].write(self.app.app.cam.view_matrix)
        self.shader_prog['model_mat'].write(self.model_mat)
    
    def destroy(self):
        [p.release() for p in self.obj.values()]
    
    def g_shader_file(self,shader):
            with open(f'./shaders/{shader}.vert') as file:
                vert_shad = file.read()
            with open(f'./shaders/{shader}.frag') as file:
                frag_shad = file.read()

            return self.app.ctx.program(vertex_shader=vert_shad,fragment_shader=frag_shad)    



