import numpy as np 
from vao import * 
from vbo import *
from shad_prog import *
import pygame as pg
import pywavefront
from abc import ABC, abstractmethod
from txuring import *
import copy



# Define an abstract base class Model
class Model(ABC):
    
    # Define the __init__() method that takes in app, txid, pos, and sh_name parameters
    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0)):
        self.app = copy.copy(app)  # sets the app attribute to app parameter
        self.pos = pos  # sets the pos attribute to pos parameter
        self.rotat = glm.vec3([glm.radians(a) for a in rotat]) #sets a rotation attribute to model
        self.ctx = app.ctx  # sets the ctx attribute to app.ctx
        self.tx = self.app.gather.tx.tx[txid] # sets the tx attribute to the texture class in txuring module with txid parameter, which is 0 or 1, and the texture file path
        
        # creates a shader program object and sets it to sh_prog_obj attribute
        self.obj = {}
        
        # sets the shader program to the shader program object
        self.shader_prog = self.app.gather.vao.new_sp
        
        # sets the model matrix to the get_model_m() method result
        self.model_mat = self.get_model_m()

    
    # Define an abstract method update()
    @abstractmethod
    def update(self):
        raise NotImplementedError

    # Define an abstract method on_init()
    @abstractmethod
    def on_init(self):
        raise NotImplementedError

    # Define an abstract method render()
    @abstractmethod
    def render(self):
        raise NotImplementedError

    # Define an abstract method destroy()
    @abstractmethod
    def destroy(self):
        raise NotImplementedError


# Define a new class named "SkyBoxModel" using the ABC module to make it an abstract base class
class SkyBoxModel(ABC):
    # Define the constructor method for the class, which is called when a new object is created
    def __init__(self, app, txid, pos=(0,0,0), sh_name="skybox"):
        # Set the app instance variable to the provided app parameter
        self.app = copy.copy(app)
        # Set the pos instance variable to the provided pos parameter (or the default value of (0,0,0) if none is provided)
        self.pos = pos
        # Set the ctx instance variable to the context associated with the provided app parameter
        self.ctx = app.ctx
        # Create a new texture object using the provided txid parameter and set it as the tx instance variable
        self.tx = self.app.gather.tx.tx[txid]
        # Create an empty dictionary object and set it as the obj instance variable
        self.obj = {}
        # Use the skybox_shader_program to load the shader program with the provided sh_name parameter and set it as the shader_prog instance variable
        self.shader_prog = self.app.gather.vao.new_sbsp
        # Use the get_model_m method to calculate the model matrix and set it as the model_mat instance variable
        self.model_mat = self.get_model_m()
        # Set the vbo instance variable to the vbo instance variable of the vbo_obj instance variable
        self.vbo = self.app.gather.vao.vbo.vbo_d['skybox']
        # Set the vao instance variable to the vao instance variable of the vao_obj instance variable
        self.vao = self.app.gather.vao.vao_arr['skybox']

    # Define an abstract update method that subclasses will need to implement
    @abstractmethod
    def update(self):
        raise NotImplementedError
    
    # Define an abstract on_init method that subclasses will need to implement
    @abstractmethod
    def on_init(self):
        raise NotImplementedError

    # Define an abstract render method that subclasses will need to implement
    @abstractmethod
    def render(self):
        raise NotImplementedError

    # Define an abstract destroy method that subclasses will need to implement
    @abstractmethod
    def destroy(self):
        raise NotImplementedError


class Cube(Model):

    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0)):
        super().__init__(app,txid,pos,sh_name,rotat)
        # creates a Vertex Buffer Object and sets it to the vbo_obj attribute
        self.vbo = self.app.gather.vao.vbo.vbo_d['cube']
        # creates a Vertex Array Object and sets it to the vao_obj attribute
        self.vao = self.app.gather.vao.vao_arr['cube']
        self.on_init()

    #model matrix
    def get_model_m(self):
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        # rotate
        model = glm.rotate(model, self.rotat.z, glm.vec3(0, 0, 1))
        model = glm.rotate(model, self.rotat.y, glm.vec3(0, 1, 0))
        model = glm.rotate(model, self.rotat.x, glm.vec3(1, 0, 0))
        return model 
    
    def update(self):
        # for moving the cube
        self.app.gather.tx.tx[0].use()  # update texture every frame
        model_mat = glm.rotate(self.model_mat,self.app.time,glm.vec3(0,1,0))
        self.shader_prog['model_mat'].write(model_mat)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['camP'].write(self.app.cam.position)

    def on_init(self):
        #bulb 
        self.shader_prog['bulb.pos'].write(self.app.bulb.pos)
        self.shader_prog['bulb.amb'].write(self.app.bulb.amb)
        self.shader_prog['bulb.spe'].write(self.app.bulb.spec)
        self.shader_prog['tx_s'] = 0
        self.app.gather.tx.tx[0].use() #  use texture
        self.shader_prog['m_proj'].write(self.app.cam.proj_matrix)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['model_mat'].write(self.model_mat)


    #render model
    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vao.release()


class Twins(Model):

    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0)):
        super().__init__(app,txid,pos,sh_name,rotat)
        # creates a Vertex Buffer Object and sets it to the vbo_obj attribute
        self.vbo = self.app.gather.vao.vbo.vbo_d['twins']
        # creates a Vertex Array Object and sets it to the vao_obj attribute
        self.vao = self.app.gather.vao.vao_arr['twins']
        self.on_init()

    #model matrix
    def get_model_m(self):
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        # rotate
        model = glm.rotate(model, self.rotat.z, glm.vec3(0, 0, 1))
        model = glm.rotate(model, self.rotat.y, glm.vec3(0, 1, 0))
        model = glm.rotate(model, self.rotat.x, glm.vec3(1, 0, 0))
        return model 
    
    def update(self):
        # for moving the cube
        self.app.gather.tx.tx[2].use()  # update texture every frame
        model_mat = glm.rotate(self.model_mat,self.app.time,glm.vec3(0,1,0))
        self.shader_prog['model_mat'].write(model_mat)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['camP'].write(self.app.cam.position)

    def on_init(self):
        #bulb 
        self.shader_prog['bulb.pos'].write(self.app.bulb.pos)
        self.shader_prog['bulb.amb'].write(self.app.bulb.amb)
        self.shader_prog['bulb.spe'].write(self.app.bulb.spec)
        self.shader_prog['tx_s'] = 0
        self.app.gather.tx.tx[2].use() #  use texture
        self.shader_prog['m_proj'].write(self.app.cam.proj_matrix)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['model_mat'].write(self.model_mat)


    #render model
    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vao.destroy()




class SkyBox(SkyBoxModel):

    def __init__(self,app,txid,pos=(0,0,0)):
        super().__init__(app,txid,pos)
        self.on_init()

    #model matrix
    def get_model_m(self):
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        return model 

    def update(self):
        self.shader_prog['v_proj'].write(glm.mat4(glm.mat3(self.app.cam.view_matrix)))

    def on_init(self):
        self.shader_prog['tx_skybox'] = 0
        self.app.gather.tx.sb.use()  #  use texture of skybox
        self.shader_prog['v_proj'].write(glm.mat4(glm.mat3(self.app.cam.view_matrix)))
        self.shader_prog['m_proj'].write(self.app.cam.proj_matrix)



    #render model
    def render(self):
        self.update()
        self.vao.render()

    def destroy(self):
        self.vao.destroy()
