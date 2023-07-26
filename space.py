# import everything from the "tri" module
from tri import *
from multiprocessing import Pool
from functools import lru_cache
from logo import *
import os,gc
import glm
from pyrr import Matrix44, Vector3
import moderngl as mgl





class Space:

    def __init__(self, app,rraw=0):
        # store a reference to the application instance
        self.app = app
        # create an empty list to hold the objects in the scene
        self.obj = []
        # create a SkyBox instance
        self.sb = SkyBox(app,0,(0,0,0))
        # load the obj
        # ects into the scene
        #run right a way,a solution to run Space class without initializing the models
        self.wtl = 'none'
        if rraw==0:
            self.wtl = input('Current models - cube,OBJ,few_cubes,few_objs ') # wtl - what to load
            self.load(self.wtl)


    def add_obj(self,cmd : list):
        try:
            avab_obj = {'cube':Cube(self.app,0,(0,0,0)),
                            'OBJ':Twins(self.app,2,(0,0,0),(270,0,0))
                            }
            model = cmd.replace("add","")[:-3]
            coord = list(cmd.replace("add","").replace(model,""))
            if model == "" or not len(coord) == 3:
                 print("Model name or coord is wrong")
            else:
                match model:
                     case 'cube':   
                        obj = Cube(self.app, 0, (int(coord[0]),int(coord[1]),int(coord[2])))
                     case 'OBJ':
                        obj = Twins(self.app, 2, (int(coord[0]),int(coord[1]),int(coord[2])),'default',(270,0,0))
                self.obj.append(obj)
        except Exception as e:
            print(e)


    # define a method to load the objects into the scene
    def load(self,wtl):
    
        match wtl:
            case 'cube':
                self.obj.append(Cube(self.app, 0, (0, 0, 0)))
            case 'OBJ':
                self.obj.append(Twins(self.app, 2, (0, -20, -50),'default',(270,0,0)))
            case 'few_cubes':
                        print('scene might take a while to load...')
                        self.obj =  self.obj + [Cube(self.app, 0, (x, 0, y)) for y in range(100) for x in range(100)]
                                  
            case 'few_objs':
                        print('scene might take a while to load...')
                        self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x),'default',(270,0,0)) for x in range(10)]
            case 'scene':
                print('loading scene...')
            case 'furmark':
                self.obj = [FurMark(self.app)]
            case _:
                  print('the model you entered is not defined.')       
        self.app.logo()
       

    #define a method to remove all objects from the scene
    def destroy(self):
        #call the "destroy" method on each object in the "obj" list
        self.sb.destroy()
        [x.destroy() for x in self.obj]


    #  define a method to render the objects in the scene
    def render(self):
        if self.wtl == 'furmark':
            for o in self.obj:
                o.render()

        else:
            # call the "render" method on the SkyBox instance
            self.sb.render()
            if len(self.obj)>0:
                camera_position = self.app.cam.position

                obj_positions = np.array([o.pos for o in self.obj])
                distances = np.linalg.norm(obj_positions - camera_position, axis=1)
                
                for o, distance in zip(self.obj, distances):
                    if distance <= self.app.cam.far_distance:
                        o.render()


        #NOTE :: looks like a working method
