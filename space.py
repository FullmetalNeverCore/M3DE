# import everything from the "tri" module
from tri import *
from multiprocessing import Pool
from functools import lru_cache
from logo import *
import os,gc
import glm
from pyrr import Matrix44, Vector3
import moderngl as mgl



#Frustum Culling 
frustum_planes = [
    glm.vec4(1, 0, 0, 1),   # Right plane
    glm.vec4(-1, 0, 0, 1),  # Left plane
    glm.vec4(0, 1, 0, 1),   # Top plane
    glm.vec4(0, -1, 0, 1),  # Bottom plane
    glm.vec4(0, 0, 1, 1),   # Near plane
    glm.vec4(0, 0, -1, 1)   # Far plane
]




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
                        self.obj =  self.obj + [Cube(self.app, 0, (x, 0, y)) for y in range(50) for x in range(50)]
                                  
            case 'few_objs':
                        print('scene might take a while to load...')
                        self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x),'default',(270,0,0)) for x in range(10)]
            case 'scene':
                print('loading scene...')
                self.obj = [Cube(self.app, 0, (0+x,0,0+y)) for x in range(50) for y in range(50)] + [Twins(self.app,2,(0,-20,-50),'default',(270,0,0))]
            case _:
                  print('the model you entered is not defined.')      
        os.system('cls' if os.name=='nt' else 'clear')     
        print(Logo.logo())     
       

    # define a method to remove all objects from the scene
    def destroy(self):
        # call the "destroy" method on each object in the "obj" list
        [x.destroy() for x in self.obj]


    # define a method to render the objects in the scene
    def render(self):
        # Get the camera position (example)
        # camera_position = self.app.cam.position  # Example camera position

        # # # Unload objects outside the render distance
        # visible_objects = []
        # for o in self.obj:
        #         obj_pos = o.pos
        #         obj_distance = np.linalg.norm(obj_pos - camera_position)
        #         if obj_distance <= self.app.cam.far_distance:
        #             visible_objects.append(o)
        # #print(f'LEN : {len(visible_objects)}')
        # print(len(visible_objects))
        # for o in visible_objects:
        #     o.render()
        # NOT WORKING   
        #print(f"                                 {len(self.obj)}",end='\r')
        camera_position = self.app.cam.position

        obj_positions = np.array([o.pos for o in self.obj])
        distances = np.linalg.norm(obj_positions - camera_position, axis=1)
        
        for o, distance in zip(self.obj, distances):
            if distance <= self.app.cam.far_distance:
                o.render() 
        #looks like a working method
        # call the "render" method on the SkyBox instance
        self.sb.render()
