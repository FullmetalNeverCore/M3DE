# import everything from the "tri" module
from components.tri import *
from multiprocessing import Pool
from functools import lru_cache
from components.logo import *
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
        self.sb = SkyBox(app,0,(0,0,0)) if self.app.uogl == 'y' else 'pass'
        # load the obj
        # ects into the scene
        #run right a way,a solution to run Space class without initializing the models
        self.wtl = 'none'
        self.models = 'cube,OBJ,few_cubes,few_objs' if self.app.uogl == 'y' else 'voxel-gen,voxel1,voxel2'
        if rraw==0:
            self.wtl = input(f'Current models - {self.models}') # wtl - what to load
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
        print(wtl)
        while True:
            if self.app.uogl == 'n':
                match wtl:
                    case 'voxel-gen':
                        self.obj = [VoxelMapRender(self.app,'gen')]
                        break
                    case 'voxel1':
                        self.obj = [VoxelMapRender(self.app,'1')]
                        break
                    case 'voxel2':
                        self.obj = [VoxelMapRender(self.app,'2')]
                        break
                    case _:
                        print('the model you entered is not defined.')   
                        wtl = input(f'Current models - {self.models}') 
                        continue 
        
            else:
                match wtl:
                    case 'cube':
                        self.obj.append(Cube(self.app, 0, (0, 0, 0)))
                        break
                    case 'OBJ':
                        self.obj.append(Twins(self.app, 2, (0, -20, -50),'default',(270,0,0)))
                        break
                    case 'few_cubes':
                                print('scene might take a while to load...')
                                self.obj =  self.obj + [Cube(self.app, 0, (x, 0, y)) for y in range(100) for x in range(100)]
                                break
                                        
                    case 'few_objs':
                                print('scene might take a while to load...')
                                self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x),'default',(270,0,0)) for x in range(10)]
                                break
                    case 'scene':
                        print('loading scene...')
                    case 'furmark':
                        self.obj = [FurMark(self.app)]
                        break
                    case _:
                        print('the model you entered is not defined.')   
                        wtl = f'Current models - {self.models}'
                        continue
        self.final = wtl
        self.app.logo()
       

    #define a method to remove all objects from the scene
    def destroy(self):
        #call the "destroy" method on each object in the "obj" list
        if self.app.uogl == 'y':self.sb.destroy()
        [x.destroy() for x in self.obj]


    #  define a method to render the objects in the scene
    def render(self):
        mods = ['voxel-gen','voxel1','voxel2','furmark']
        if self.final in mods:
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
