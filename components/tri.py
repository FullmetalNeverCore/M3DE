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
from components.wrld import *


#TODO:Instancing


# Define an abstract base class3 Model
class Model(ABC):
    
    
    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0)):
        self.app = app  # sets the app attribute to app parameter
        self.pos = pos  # sets the pos attribute to pos parameter
        self.rotat = glm.vec3([glm.radians(a) for a in rotat]) #sets a rotation attribute to model
        self.ctx = app.ctx  # sets the ctx attribute to app.ctx
        self.tx = self.app.gather.tx.tx[txid] # sets the tx attribute to the texture class in txuring module with txid parameter, which is 0 or 1, and the texture file path
        self.base_vao = self.app.gather.vao
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
        self.app = app
        # Set the pos instance variable to the provided pos parameter (or the default value of (0,0,0) if none is provided)
        self.pos = pos
        # Set the ctx instance variable to the context associated with the provided app parameter
        self.ctx = app.ctx
        # Create a new texture object using the provided txid parameter and set it as the tx instance variable
        self.tx = self.app.gather.tx.tx[txid]
        # Create an empty dictionary object and set it as the obj instance variable
        self.obj = {}
        self.model_mat = self.get_model_m()
        # Use the skybox_shader_program to load the shader program with the provided sh_name parameter and set it as the shader_prog instance variable
        self.shader_prog = self.app.gather.vao.new_sbsp
        # Set the vbo instance variable to the vbo instance variable of the vbo_obj instance variable
        self.vbo = self.app.gather.vao.vbo.vbo_d['skybox']
        # Set the vao instance variable to the vao instance variable of the vao_obj instance variable
        self.base_vao = self.app.gather.vao
        self.vao = self.base_vao.vao_arr['skybox']

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

    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0))->None:
        super().__init__(app,txid,pos,sh_name,rotat)
        # creates a Vertex Buffer Object and sets it to the vbo_obj attribute
        self.vbo = self.app.gather.vao.vbo.vbo_d['cube']
        # creates a Vertex Array Object and sets it to the vao_obj attribute
        self.vao = self.base_vao.vao_arr['cube']
        self.on_init()

    #model matrix
    def get_model_m(self)->None:
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        # rotate
        # model = glm.rotate(model, self.rotat.z, glm.vec3(0, 0, 1))
        # model = glm.rotate(model, self.rotat.y, glm.vec3(0, 1, 0))
        # model = glm.rotate(model, self.rotat.x, glm.vec3(1, 0, 0))
        return model 
    


    def update(self)->None:
        # for moving the cube
        self.app.gather.tx.tx[0].use()  # update texture every frame
        self.shader_prog['model_mat'].write(self.model_mat)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['camP'].write(self.app.cam.position)
        

    def on_init(self)->None:
        #bulb 
        self.shader_prog['bulb.pos'].write(self.app.bulb.pos)
        self.shader_prog['bulb.amb'].write(self.app.bulb.amb)
        self.shader_prog['bulb.spe'].write(self.app.bulb.spec)
        self.shader_prog['tx_s'] = 0
        self.app.gather.tx.tx[0].use() #  use texture
        self.shader_prog['m_proj'].write(self.app.cam.proj_matrix)
        ##self.ctx.enable(moderngl.CLIP_DISTANCE0)
        #self.ctx.clip_control(moderngl.LOWER_LEFT, moderngl.NEGATIVE_ONE_TO_ONE)
        #self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        #self.shader_prog['model_mat'].write(self.model_mat)


    #render model
    def render(self)->None:
        #if datetime.datetime.now().second % 2 == 0:
        self.update()
        self.vao.render()

    def destroy(self)->None:
        self.base_vao.destroy()



class Twins(Model):

    def __init__(self,app,txid,pos=(0,0,0),sh_name="default",rotat=(0, 0, 0))->None:
        super().__init__(app,txid,pos,sh_name,rotat)
        # creates a Vertex Buffer Object and sets it to the vbo_obj attribute
        self.vbo = self.app.gather.vao.vbo.vbo_d['twins']
        # creates a Vertex Array Object and sets it to the vao_obj attribute
        self.vao = self.base_vao.vao_arr['twins']
        self.on_init()

    #model matrix
    def get_model_m(self)->None:
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        # rotate
        model = glm.rotate(model, self.rotat.z, glm.vec3(0, 0, 1))
        model = glm.rotate(model, self.rotat.y, glm.vec3(0, 1, 0))
        model = glm.rotate(model, self.rotat.x, glm.vec3(1, 0, 0))
        return model 
    
    def update(self)->None:
        # for moving the cube
        self.app.gather.tx.tx[2].use()  # update texture every frame
        #model_mat = glm.rotate(self.model_mat,self.app.time,glm.vec3(0,0,0))
        self.shader_prog['model_mat'].write(self.model_mat)
        self.shader_prog['v_proj'].write(self.app.cam.view_matrix)
        self.shader_prog['camP'].write(self.app.cam.position)

    def on_init(self)->None:
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
    def render(self)->None:
        self.update()
        self.vao.render()

    def destroy(self)->None:
        self.base_vao.destroy()




class SkyBox(SkyBoxModel):

    def __init__(self,app,txid,pos=(0,0,0)):
        super().__init__(app,txid,pos)
        self.on_init()

    #model matrix
    def get_model_m(self)->None:
        model = glm.mat4()
        model = glm.translate(model,self.pos)
        return model 


    def update(self)->None:
        #time * speed
        model_mat = glm.rotate(self.model_mat,self.app.time*0.01,glm.vec3(0,0.1,0))
        self.shader_prog['model_mat'].write(model_mat)
        self.shader_prog['v_proj'].write(glm.mat4(glm.mat3(self.app.cam.view_matrix)))

    def on_init(self)->None:
        self.shader_prog['tx_skybox'] = 0
        self.app.gather.tx.sb.use()  #  use texture of skybox
        self.shader_prog['v_proj'].write(glm.mat4(glm.mat3(self.app.cam.view_matrix)))
        self.shader_prog['m_proj'].write(self.app.cam.proj_matrix)



    #render model
    def render(self)->None:
        self.update()
        self.vao.render()

    def destroy(self)->None:
        self.base_vao.destroy()


#Becnhmark
class FurMark():

    def __init__(self, app)->None:
        self.app = app
        self.vert = self.app.ctx.buffer(
            np.array([
                -1.0, -1.0,
                1.0, -1.0,
                -1.0,  1.0,
                1.0,  1.0,
            ], dtype=np.float32).tobytes())
        self.shad_prog = self.app.gather.vao
        self.fursp = self.shad_prog.sp.obj['furmark']  # shader program, vertex and fragment shader here
        self.vao = self.app.ctx.vertex_array(self.fursp, [(self.vert, '2f', 'in_vert')])

    def destroy(self)->None:
        self.shad_prog.sp.destroy()

    def update(self)->None:
        self.fursp['time'] = self.app.time
        self.fursp['tx_s'] = 0  # Set the texture sampler value to 0 for the default texture unit
        self.app.gather.tx.tx[3].use()  # Use texture of skybox on texture unit 0
        self.fursp['noise'] = 1
        self.app.gather.tx.tx[4].use(location=1)
        self.fursp['backg'] = 2 
        self.app.gather.tx.tx[5].use(location=2)
        
    def render(self)->None:
        self.update()
        self.app.ctx.clear()
        self.vao.render(mgl.TRIANGLE_STRIP)


class VoxelMapRender():

    def __init__(self, app,mode='gen')->None:
        self.app = app
        noise = Perlin().generate_and_visualize_maps(1024, 1024, 200, 34, 0.4, 4, save_path="./tx/maps/")
        maps = [[f'./tx/maps/height_map_{noise}.png',f'./tx/maps/color_map_{noise}.png'],
                [f'./tx/maps/height_map_1.png',f'./tx/maps/color_map_1.png']]

        #height/color  generation or map loading 
        if mode == 'gen':
            h_map_img = pg.image.load(maps[0][0]) 
            c_map_img = pg.image.load(maps[0][1]) 
        else:
            h_map_img = pg.image.load(maps[1][0]) 
            c_map_img = pg.image.load(maps[1][1])         
        self.hmap = pg.surfarray.array3d(h_map_img)
        self.cmap = pg.surfarray.array3d(c_map_img)
        self.mheight =  len(self.hmap[0])
        self.mwidth = len(self.hmap)
        self.cam = Cam(self.app)


    #NO OGL ,NO NEED TO DESTROY OBJECTS
    def destroy(self)->None:
        pass

    
    def update(self)->None:
        self.cam.update()
        self.cam.screen_array = Raycasting.raycasting(self.cam.screen_array,self.mheight,self.mwidth,self.hmap,
                                           self.cmap,self.cam.campos,
                                           self.cam.cam_angle,self.cam.camheight,
                                           self.cam.campitch,self.app.WIN_SIZE[0],
                                           self.app.WIN_SIZE[1],self.cam.delta_angle,
                                           self.cam.ray_dist,self.cam.rhfov,
                                           self.cam.scale)

    def render(self)->None:
        #make surface out of array.
        self.update()
        self.app.screen.blit(pg.surfarray.make_surface(self.cam.screen_array),(0,0))


class Minecraft():
    def __init__(self,app)->None:
        self.app = app
        self.shad_prog = self.app.gather.sp
        self.minesp = self.app.gather.minesp # shader program, vertex and fragment shader here
        self.world = self.app.gather.world
        self.tx = self.app.gather.tx.tx[6]
        self.on_init()

    def update(self)->None:
        self.minesp['v_proj'].write(self.app.cam.view_matrix)
        self.minesp['camP'].write(self.app.cam.position)
        self.minesp['rendist'].write(glm.int32(int(self.app.cam.far_distance)))
        self.tx.use(location=0)

    def render(self)->None:
        self.update()
        self.world.render()

    def destroy(self)->None:
        self.shad_prog.destroy()

    def on_init(self)->None:
        self.minesp['tx_0'] = 0 
        self.tx.use(location=0)
        self.minesp['m_proj'].write(self.app.cam.proj_matrix)

