import pygame as pg
import moderngl as mgl
import sys
from components.tri import *
from components.cam import Cam
from components.bulb import Bulb
from components.space import *
import os
from components.logo import *
import psutil
from components.gather import *
from OpenGL.GL import *
import components.local_neofetch
import cpuinfo
import platform
import subprocess
if platform.system() == 'Windows':
     import msvcrt
else:
    import getch
    import selectors
    import aioconsole
import threading
import components.points 
import numba


class M3DE:
    def __init__(self, win_size=(1280,720),uoglcmd=0,rraw=0,dev=0) -> None:
        self.dev = dev
        self.uoglcmd = uoglcmd
        self.status = 'run'
        if (uoglcmd == 1 and not rraw == 0):
            self.uogl =  input("Deactivate VoxelEngine? (y/n)")#use opengl?
        elif (uoglcmd == 1 and rraw == 0):
            self.uogl = 'n'
            self.status = 'voxel'
        else:
            self.uogl = 'y'
        if self.uogl == 'n':print('WARNING: Without OGL some scenes will not work!')
        pg.init()
        #PyGame mouse
        pg.event.set_grab(True) #make mouse operate inside the window
        pg.mouse.set_visible(False) #setting cursor invisible
        # OpenGL attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE,24)
        pg.display.set_caption("M3DE")
        # Window size
        self.WIN_SIZE = win_size
        # Create OpenGL context
        if self.uogl == 'y':
            self.screen = pg.display.set_mode(self.WIN_SIZE, flags= pygame.OPENGL| pg.DOUBLEBUF)
        else:
            self.screen = pg.display.set_mode(self.WIN_SIZE,pg.SCALED)
        # Detect and use existing OpenGL context
        #glViewport(0, 0, 1280, 700) # OpenGL render screen size
        if self.uogl == 'y':
            self.ctx = mgl.create_context()
            self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND) # CULL_FACE to not render invisible
            self.ctx.gc_mode = 'auto'
        self.config = components.local_neofetch.HardwareStat().template()
        # Time
        self.time = 0
        self.d_time = 0
        self.cli_dump = []
        self.bench = components.points.Benchmark()
        self.ram_usage = self.get_process_stats()
        # Framerate and delta time   
        self.clock = pg.time.Clock()
        self.finish = False 
        self.stop_event = threading.Event()


    def logo(self,conf=0):
                        os.system('cls' if os.name=='nt' else 'clear')   
                        print(Logo.logo())  
                        if conf == 0:print(self.config)


    #linux solution
    def get_cpu_temperature(self)->str:
        if not platform.system() == 'windows':
            try:
                output = subprocess.check_output(["sensors"])
                for line in output.splitlines():
                    line = line.decode()
                    if "Core" in line:
                        temperature_str = line.split(":")[-1].strip().split(" ")[0]
                        return temperature_str
            except Exception as e:
                return str(e)
        else:
            return 'No windows solution was implemented for now.'

    # Method for handling events
    def events(self):
        for event in pg.event.get():
            if (event.type == pg.KEYDOWN and event.key == pg.K_z) or event.type == pg.QUIT:
                self.space.destroy()
                if self.uogl == 'y':self.gather.destroy()
                pg.quit()
                sys.exit()
            elif (event.type == pg.KEYDOWN and event.key == pg.K_x):
                self.space.destroy()
                if self.uogl == 'y':self.gather.destroy()
                self.run()

    # Method for getting time
    def space_time(self):
        self.time = pg.time.get_ticks() * 0.001
         
    def benchmark_sched(self):
        #pg.quit()
        print('Benchmarking complete.')
        print(f'Avarage FPS: {self.bench.avarage_fps()}')
        print(f'PC score: {self.bench.count_points()}')
        self.finish = True
        self.stop_event.set()


    # Method for rendering the scene
    def render_scene(self):
        if self.space.wtl == 'furmark':
            self.bench.fps_count.append(self.clock.get_fps())
        print(f"\rRAM usage: {self.ram_usage:.2f} MB | FPS: {int(self.clock.get_fps())} | input : {self.cli_dump}", end='\r') 
        if self.uogl == 'y':
            self.ctx.clear(color=(0,0,0))
        self.space.render()
        pg.display.flip()

    # Function to get CPU utilization and RAM consumption
    def get_process_stats(self)->float:
        pid = os.getpid()
        process = psutil.Process(pid)
        mem_info = process.memory_info()
        ram_usage = mem_info.rss / (1024 * 1024)  # convert to MB
        return ram_usage

    
    def cli_linux(self):
                selec = selectors.DefaultSelector()
                selec.register(sys.stdin,selectors.EVENT_READ)
                events = selec.select(timeout=0.001)
                # print(f"{sys.stdin.readline().strip()}",end='\r')
                if events:
                        e = sys.stdin.readline().strip()
                        if 'test' in e:
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(Logo.logo())
                            print('test')
                            self.cli_dump = []
                        elif 'stop' in e:
                            #[x.destroy() for x in self.space.obj]
                            self.space.obj = []
                            self.space.wtl = input('Current models - cube,OBJ,few_cubes,few_objs ')
                            self.space.load(self.space.wtl)
                        elif 'add' in e:
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(Logo.logo())
                            print('ADDING OBJECT TO RENDER ARRAY')
                            self.space.add_obj(e)
                            self.cli_dump = []
                        self.cli_dump.append(e)
                


    def cli(self):
        try:
            if platform.system() == "Windows":
                if msvcrt.kbhit():
                    user_input = msvcrt.getch()
                    if ord(user_input) == 13:
                        if 'test' in ''.join(self.cli_dump):
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(Logo.logo())
                            print('test')
                            self.cli_dump = []
                        elif 'add' in ''.join(self.cli_dump):
                            os.system('cls' if os.name=='nt' else 'clear')
                            print(Logo.logo())
                            print('ADDING OBJECT TO RENDER ARRAY')
                            self.space.add_obj(''.join(self.cli_dump))
                            self.cli_dump = []
                    else:
                            user_input = user_input.decode('utf-8').strip()
                            if user_input[0] == '\x08':
                                self.logo()
                                try:
                                    self.cli_dump.remove(self.cli_dump[len(self.cli_dump)-1])
                                except IndexError:
                                    print('Nothing to delete')
                            else:
                                # print(self.cli_dump)
                                self.cli_dump.append(user_input[0])
        except Exception as e:
             print(e)


    # Main loop of the program
    def run(self,rraw=0):
        match self.dev:
            case 1:
                print('DEVELOPMENT MODE')
        if rraw==1:
            self.status = 'benchmark'
        self.logo(1)
        # Camera
        # print(self.status)
        self.cam = Cam(self,input("Draw distance: ") if not self.status in ['benchmark','voxel'] else 0)
        if self.uogl == 'y':
            # LIGHT
            if not self.status == 'benchmark':
                self.bulb = Bulb()
            # Triangles 
            #Gather
            self.gather = Gather(self)  
        if rraw == 0:
                self.space = Space(self)
        else:
            self.space = Space(self,1)
            self.space.wtl = 'furmark'
            self.space.load(self.space.wtl)
        if self.space.wtl == 'furmark':
            #Benchmarking
            thrd = threading.Timer(15,self.benchmark_sched)
            thrd.daemon = True  
            thrd.start()   
        while True:
            if self.finish:
                 print('Finished!')
                 sys.exit()
            self.space_time()
            self.events()
            self.cam.update()
            self.render_scene()
            if platform.system() == 'Windows':
                self.cli()
            else:
                self.cli_linux()
            self.d_time = self.clock.tick(500)

# Main entry point of the program
if __name__ == '__main__':
    print(sys.argv)
    M3DE(uoglcmd=1 if '-voxel' in sys.argv else 0,
    rraw=1 if '-bm' in sys.argv else 0,dev=1 if '-dev' in sys.argv else 0).run(rraw=1 if '-bm' in sys.argv else 0)
