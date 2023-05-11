# import everything from the "tri" module
from tri import *
from multiprocessing import Pool
from functools import lru_cache
from logo import *
import os,gc

# define a class called "Space"
class Space:
    # define the constructor for the class
    def __init__(self, app):
        # store a reference to the application instance
        self.app = app
        # create an empty list to hold the objects in the scene
        self.obj = []
        # create a SkyBox instance, passing in the application instance, an ID of 0, and the color black
        self.sb = SkyBox(app,0,(0,0,0))
        # load the obj
        # ects into the scene
        wtl = input('Current models - cube,OBJ,few_cubes,few_objs ') # wtl - what to load
        self.load(wtl)

    @lru_cache(maxsize=None)
    def get_cube(self,x):
       return Cube(self.app, 0, (0+x, 0-x, 0+x))

    # define a method to load the objects into the scene
    def load(self,wtl):
        # create 10 Cube instances, each with a unique position along the x-axis, and add them to the "obj" list
        match wtl:
            case 'cube':
                self.obj.append(Cube(self.app, 0, (0, 0, 0)))
            case 'OBJ':
                self.obj.append(Twins(self.app, 2, (0, -20, -50),'default',(270,0,0)))
            case 'few_cubes':
                        print('scene might take a while to load...')
                        self.obj = [Cube(self.app, 0, (x, 2, y)) for x in range(-30,30,2) for y in range(-30,30,2)]
                                  
            case 'few_objs':
                        print('scene might take a while to load...')
                        self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x),'default',(270,0,0)) for x in range(10)]
            case _:
                  print('the model you entered is not defined.')      
        os.system('cls' if os.name=='nt' else 'clear')     
        print(Logo.logo())     
       

    # define a method to remove all objects from the scene
    def destroy(self):
        # call the "destroy" method on each object in the "obj" list
        [x.destroy() for x in self.obj]
        gc.collect()

    # define a method to render the objects in the scene
    def render(self):
        # loop through each object in the "obj" list and call its "render" method
        for o in self.obj:
            o.render()
        # call the "render" method on the SkyBox instance
        self.sb.render()
