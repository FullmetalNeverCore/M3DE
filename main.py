import pygame as pg 
import moderngl as mgl
import sys
from tri import *
from cam import Cam
from bulb import Bulb
from space import *

class M3DE:
    def __init__(self, win_size=(1600,900)) -> None:
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
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE) # CULL_FACE to not render invisible
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
        self.ctx.clear(color=(0,0,0))
        self.space.render()
        pg.display.flip()

    # Main loop of the program
    def run(self):
        print('''
        ███╗   ███╗██████╗ ██████╗ ███████╗
        ████╗ ████║╚════██╗██╔══██╗██╔════╝
        ██╔████╔██║ █████╔╝██║  ██║█████╗  
        ██║╚██╔╝██║ ╚═══██╗██║  ██║██╔══╝  
        ██║ ╚═╝ ██║██████╔╝██████╔╝███████╗
        ╚═╝     ╚═╝╚═════╝ ╚═════╝ ╚══════╝
                                   0xNC @ 2023             
        
        ''')
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
