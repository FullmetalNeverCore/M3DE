import numpy as np 
from vao import * 
from vbo import *
from shad_prog import *
import pygame as pg
import pywavefront


class Tri:
    def __init__(self,app):
        self.app = app 
        self.ctx = app.ctx
        self.vbo = tri_VBO(self).vbo
        self.shader_prog = shader_program(self).shader_prog
        self.vao = tri_VAO(self).vao


    #render model
    def render(self):
        self.vao.render()

class Cube:

    def __init__(self,app,pos=(0,0,0)):
        self.app = app 
        self.pos = pos
        self.ctx = app.ctx
        self.tx = self.texturing('./tx/dirt.jpg')

        self.vbo_obj = cube_VBO(self)
        self.vbo = self.vbo_obj.vbo
        self.sh_prog_obj = shader_program(self)
        self.shader_prog = self.sh_prog_obj.shader_prog
        self.vao_obj = cube_VAO(self)
        self.vao = self.vao_obj.vao
        
    def texturing(self,path):
        tx = pg.image.load(path).convert()
        tx = pg.transform.flip(tx,flip_x=False,flip_y=True)
        return self.ctx.texture(tx.get_size(),3,pg.image.tostring(tx,'RGB'))

    #render model
    def render(self):
        self.sh_prog_obj.update()
        self.vao.render()

    def destroy(self):
        self.vbo_obj.destroy()
        self.vao_obj.destroy()
        self.sh_prog_obj.destroy()


class Twins:
    def __init__(self,app,pos=(0,0,0)):
        self.app = app 
        self.pos = pos
        self.ctx = app.ctx
        self.tx = self.texturing('./tx/model.jpg')

        self.vbo_obj = twins_VBO(self)
        self.vbo = self.vbo_obj.vbo
        self.sh_prog_obj = shader_program(self)
        self.shader_prog = self.sh_prog_obj.shader_prog
        self.vao_obj = twins_VAO(self)
        self.vao = self.vao_obj.vao
        
    def texturing(self,path):
        tx = pg.image.load(path).convert()
        tx = pg.transform.flip(tx,flip_x=False,flip_y=True)
        return self.ctx.texture(tx.get_size(),3,pg.image.tostring(tx,'RGB'))

    #render model
    def render(self):
        self.sh_prog_obj.update()
        self.vao.render()

    def destroy(self):
        self.vbo_obj.destroy()
        self.vao_obj.destroy()
        self.sh_prog_obj.destroy()