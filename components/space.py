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
        self.models = 'cube,OBJ,few_cubes,few_cubes2,mc ' if self.app.uogl == 'y' else 'voxel-gen,voxel1,voxel2'
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
                match model.lower():
                     case 'cube':   
                        obj = Cube(self.app, 0, (int(coord[0]),int(coord[1]),int(coord[2])))
                     case 'obj':
                        obj = Twins(self.app, 2, (int(coord[0]),int(coord[1]),int(coord[2])),'default',(270,0,0))
                self.obj.append(obj)
        except Exception as e:
            print(e)


    # define a method to load the objects into the scene
    def load(self,wtl : str):
        # print(wtl)
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
                        self.obj.append(Cube(self.app, 0, glm.vec3(0, 0, 0)))
                        break
                    case 'OBJ':
                        self.obj.append(Twins(self.app, 2, (0, -20, -50),'default',(270,0,0)))
                        break
                    case 'few_cubes':
                                print('scene might take a while to load...')
                                size = 50  # Adjust the size of the pyramid
                                self.app.cam.position = glm.vec3(12,12,68)
                                for y in range(size):
                                    for x in range(y, size-y):
                                        for z in range(y, size-y):
                                            self.obj.append(Cube(self.app, 0, (x, y, z)))
                                break
                                        
                    case 'few_cubes2':
                                size = 50
                                self.app.cam.position = glm.vec3(12,12,68)
                                for y in range(size):
                                    for x in range(y, size - y):
                                        for z in range(y, size - y):
                                            if (y == 0 or y == size - 1 or x == y or x == size - y - 1 or z == y or z == size - y - 1):
                                                self.obj.append(Cube(self.app, 0, (x, y, z)))
                                break
                    case 'scene':
                        print('loading scene...')
                    case 'furmark':
                        self.obj = [FurMark(self.app)]
                        break
                    case 'mc':
                        self.app.cam.position = glm.vec3(445, 23, 418) 
                        self.obj.append(Twins(self.app, 2, (439,5,354),'default',(270,0,0)))
                        self.obj.append(Minecraft(self.app))
                        break
                    case _:
                        print('the model you entered is not defined.')   
                        wtl = f'Current models - {self.models}'
                        continue
        self.final = wtl
        self.app.logo()
       

    #trying to define collision method
    def destroy(self):
        #call the "destroy" method on each object in the "obj" list
        if self.app.uogl == 'y':self.sb.destroy()
        [x.destroy() for x in self.obj]

    #test 
    def is_point_inside_cube(self,point_coords, cube_position, cube_size):
        min_cube_coords = glm.vec3(cube_position)
        max_cube_coords = glm.vec3(cube_position) + (1.0,1.0,1.0)

        if (min_cube_coords.x <= point_coords.x <= max_cube_coords.x and
            min_cube_coords.y <= point_coords.y <= max_cube_coords.y and
            min_cube_coords.z <= point_coords.z <= max_cube_coords.z):
            return True
        else:
            return False

    #  define a method to render the objects in the scene
    def render(self):
        mods = ['voxel-gen','voxel1','voxel2','furmark','mc']
        if not self.final in ['voxel-gen','voxel1','volel2']:
            self.sb.render() 
        if self.final in mods:
            for o in self.obj:
                o.render()

        else:
            # call the "render" method on the SkyBox instance
            match self.app.dev:
                case 1:
                    # print(self.is_point_inside_cube(self.app.cam.position,(0,0,0),(1,1,1)))
                    print(self.app.cam.position,end="\r")
                    # print(glm.vec3((0,0,0)) + (0.12,0.12,0.12))
            if len(self.obj)>0:
                camera_position = self.app.cam.position

                obj_positions = np.array([o.pos for o in self.obj])
                distances = np.linalg.norm(obj_positions - camera_position, axis=1)
                
                for o, distance in zip(self.obj, distances):
                    if distance <= self.app.cam.far_distance:
                        o.render()


        #NOTE :: looks like a working method
