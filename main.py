import pygame as pg 
import moderngl as mgl
import sys
from tri import *
from cam import Cam
from bulb import Bulb


class M3DE:
    def __init__(self, win_size=(1600,900)) -> None:
        pg.init()
        #ogl attrs 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
        #window size
        self.WIN_SIZE = win_size
        #create opengl context
        pg.display.set_mode(self.WIN_SIZE,flags=pg.OPENGL | pg.DOUBLEBUF)
        # detect and use existing opengl context
        self.ctx = mgl.create_context() 
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE) # CULL_FACE not render invisible
        #time 
        self.time = 0
        self.delta_time = 0
        #cam
        self.cam = Cam(self)
        #LIGHT
        self.bulb = Bulb()
        #tri2 
        self.tri2 = Cube(self,(1,0,0))
        #framerate and delta time   
        self.clock = pg.time.Clock()
        

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.tri.destroy()
                pg.quit()
                sys.exit()
    
    #getting time
    def space_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def render_scene(self):
        self.ctx.clear(color=(0,0,0))
        self.tri2.render()
        pg.display.flip()
    
    
    def run(self):
        while True:
            self.space_time()
            self.events()
            self.cam.update()
            self.render_scene()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    m3de = M3DE()
    m3de.run()
    