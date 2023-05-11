import pygame as pg 
import moderngl as mgl
import sys
from tri import *
from cam import Cam
from bulb import Bulb
from space import *
import os
from logo import *
import psutil

class M3DE:
    def __init__(self, win_size=(800,600)) -> None:
        pg.init()
        # OpenGL attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
        # Window size
        self.WIN_SIZE = win_size
        # Font
        self.font = pg.font.SysFont(None, 25)
        # Create OpenGL context
        self.screen = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # Detect and use existing OpenGL context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST) # CULL_FACE to not render invisible
        # Time
        self.time = 0
        self.delta_time = 0
        # Framerate and delta time   
        self.clock = pg.time.Clock()


    # Method for handling events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.space.destroy()
                pg.quit()
                sys.exit()
    
    # Method for getting time
    def space_time(self):
        self.time = pg.time.get_ticks() * 0.001

    # Method for rendering the scene
    def render_scene(self):
        ram_usage = self.get_process_stats()

        print(f"           RAM usage: {ram_usage:.2f} MB",end='\r')
        print(f' FPS:{int(self.clock.get_fps())}',end='\r')
        self.ctx.clear(color=(0,0,0))
        self.space.render()
        pg.display.flip()

    # Method for rendering text
    def render_text(self, text, position):
        text_surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    # function to get CPU utilization and RAM consumption
    def get_process_stats(self):
        pid = os.getpid()
        process = psutil.Process(pid)
        mem_info = process.memory_info()
        ram_usage = mem_info.rss / (1024 * 1024)  # convert to MB
        return ram_usage

    # Main loop of the program
    def run(self):
        os.system('cls' if os.name=='nt' else 'clear')
        print(Logo.logo())
        input('press enter to start')
        # Camera
        self.cam = Cam(self)
        # LIGHT
        self.bulb = Bulb()
        # Triangles 
        self.space = Space(self)
        while True:
            self.space_time()
            self.events()
            self.cam.update()
            self.render_scene()
            self.delta_time = self.clock.tick(60)

# Main entry point of the program
if __name__ == '__main__':
    m3de = M3DE()
    m3de.run()
