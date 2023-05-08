# import everything from the "tri" module
from tri import *

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
                        self.obj = [Cube(self.app, 0, (0+x, 0-x, 0+x)) for x in range(10)]
                        self.obj = [Cube(self.app, 0, (0-x, 0-x, 0+x)) for x in range(10)]
            case 'few_obj':
                        print('scene might take a while to load...')
                        self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x)) for x in range(10)]
                        self.obj = [Twins(self.app, 2, (0+x, 0-x, 0+x)) for x in range(10)] 
            case _:
                  print('the model you entered is not defined.')                
       

    # define a method to remove all objects from the scene
    def destroy(self):
        # call the "destroy" method on each object in the "obj" list
        [x.destroy() for x in self.obj]

    # define a method to render the objects in the scene
    def render(self):
        # loop through each object in the "obj" list and call its "render" method
        for o in self.obj:
            o.render()
        # call the "render" method on the SkyBox instance
        self.sb.render()
