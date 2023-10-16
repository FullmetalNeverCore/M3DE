import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod
from components.chunk import *


# Define an abstract base class for VBO interfaces
class VBO_interface(ABC):
    
    # Define an abstract method for retrieving vertex data
    @abstractmethod
    def vert_data(self)->'Vertex Data':
        raise NotImplementedError
    
    
    # Define an abstract method for retrieving the OpenGL VBO handle
    @abstractmethod
    def g_vbo(self)->'Buffer':
        raise NotImplementedError


class general_VBO:
    def __init__(self,vao,app) -> None:
        self.app = app
        self.vao = vao
        self.chunk = Chunk(self.app)
        self.vbo_d = {
            'cube' : cube_VBO(app),
            'skybox' : skybox_VBO(app),
            'twins' : twins_VBO(app),
            'minecraft' : minecraft_VBO(app,self.chunk,self.vao)
        }



# Define a concrete subclass of VBO_interface for skybox VBOs
class skybox_VBO(VBO_interface):
    
    # Constructor method for the skybox VBO
    def __init__(self, app):
        self.app = app # Retrieve the OpenGL VBO handle


    # method to generate geometry data from vertex and index arrays
    def g_data(self,vert, ind):
        return np.array([vert[i] for tri in ind for i in tri], dtype='f4')

    # Implement the vert_data method to retrieve the vertex data for the skybox
    def vert_data(self) -> list:
        # Define the vertex data and index arrays for the skybox
        vert_data = [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),
                     (-1,1,-1),(-1,-1,-1),(1,-1,-1),(1,1,-1)]
        ind = [(0,2,3),(0,1,2),
               (1,7,2),(1,6,7),
               (6,5,4),(4,7,6),
               (3,4,5),(3,5,0),
               (3,7,4),(3,2,7),
               (0,6,1),(0,5,6)]
        
        # Generate the geometry data using the g_data static method
        geom_data = np.flip(self.g_data(vert_data,ind),1).copy(order='C')
        
        return geom_data

    # Implement the g_vbo method to retrieve the OpenGL VBO handle for the skybox
    def g_vbo(self):
        # Retrieve the vertex data and create an OpenGL VBO using the app context
        return self.app.ctx.buffer(self.vert_data())
    
class cube_VBO(VBO_interface):
    def __init__(self,app):
        # Constructor for the cube_VBO class
        # Initializes app and vbo attributes
        self.app = app 

    def g_data(self,vert,ind):
        # method to convert vertex and index data into numpy array
        # Returns a numpy array containing the vertex data in the order specified by the index data
        return np.array([vert[i] for tri in ind for i in tri],dtype='f4')

    def vert_data(self) -> list:
        # Generates the vertex data for a cube
        # Returns a list of vertex coordinates
        cube_offset = 0
        # vert_data = [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),
        #              (-1,1,-1),(-1,-1,-1),(1,-1,-1),(1,1,-1)]
        vert_data = []
        cube_size = 1
                    # Calculate the position of each cube based on the offset
        x = cube_offset
        y = cube_offset
        z = cube_offset

                    # Generate the vertex coordinates for the current cube
        cube_verts = [
                        (x - cube_size, y - cube_size, z + cube_size),
                        (x + cube_size, y - cube_size, z + cube_size),
                        (x + cube_size, y + cube_size, z + cube_size),
                        (x - cube_size, y + cube_size, z + cube_size),
                        (x - cube_size, y + cube_size, z - cube_size),
                        (x - cube_size, y - cube_size, z - cube_size),
                        (x + cube_size, y - cube_size, z - cube_size),
                        (x + cube_size, y + cube_size, z - cube_size)
                    ]

        vert_data.extend(cube_verts)
        # Specifies the indices for the triangles that make up the cube
        ind = [(0,2,3),(0,1,2),
               (1,7,2),(1,6,7),
               (6,5,4),(4,7,6),
               (3,4,5),(3,5,0),
               (3,7,4),(3,2,7),
               (0,6,1),(0,5,6)]
        
        # Specifies texture coordinates for each vertex
        tx_coord = [(0,0),(1,0),(1,1),(0,1)]
        
        # Specifies the indices for the texture coordinates
        tx_coord_ind = [(0,2,3),(0,1,2),
                        (0,2,3),(0,1,2),
                        (0,1,2),(2,3,0),
                        (2,3,0),(2,0,1),
                        (0,2,3),(0,1,2),
                        (3,1,2),(3,0,1),
                        ]
        
        # Specifies the normals for each face of the cube
        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        
        # Convert the normals, vertex data and texture coordinates into numpy arrays and concatenate them into one array
        normals = np.array(normals, dtype='f4').reshape(36, 3)
        geom_data = self.g_data(vert_data,ind)
        tex_data = self.g_data(tx_coord,tx_coord_ind)

        geom_data = np.hstack([normals,geom_data])
        geom_data = np.hstack([tex_data,geom_data])

        # Returns the concatenated array of vertex, texture and normal data
        return geom_data

    def g_vbo(self):
        # Generates a Vertex Buffer Object (VBO) from the vertex, texture and normal data generated by the vert_data method
        return self.app.ctx.buffer(self.vert_data())



class twins_VBO(VBO_interface):
    def __init__(self,app):
        self.app = app 

    def vert_data(self):
        # Load the 3D model using PyWavefront
        objs = pywavefront.Wavefront('./model/12221_Cat_v1_l3.obj', cache=True, parse=True)
        
        # Take the first material of the model and get its vertices
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        
        # Convert the vertices to a numpy array of 32-bit floats
        vertex_data = np.array(vertex_data, dtype='f4')
        
        # Return the vertex data as a 1D array
        return vertex_data

    def g_vbo(self):
        # Generate a Vertex Buffer Object and store the vertex data in it
        return self.app.ctx.buffer(self.vert_data())


class minecraft_VBO(VBO_interface):
    def __init__(self,app,ch,vao):
        self.app = app 
        self.vao = vao 
        self.chunk = ch #ch - chunk

    
    def add_data(self,vert_data,ind,*vertecies)->int:
        for vert in vertecies:
            for a in vert:
                vert_data[ind] = a
                ind += 1
        return ind #giving number of next pos
        
    def chunk_mesh(self,voxle_data,format_s)->np.array:
        vertex_data = np.empty(self.chunk.chunk_vol*18*5*format_s,dtype='uint8')
        ind = 0 
        for x in range(self.chunk.chunk_size):
            for y in range(self.chunk.chunk_size):
                for z in range(self.chunk.chunk_size):
                    voxid = voxle_data[x+self.chunk.chunk_size*z+self.chunk.chunk_area*y]
                    if not voxid:
                        continue
                    #Cheking if side is visible to camera
                    #top of the block
                    if self.check_emp((x,y + 1,z),voxle_data):
                        e0 = (x,y+1,z,voxid,0)
                        e1 = (x+1,y+1,z,voxid,0)
                        e2 = (x+1,y+1,z+1,voxid,0)
                        e3 = (x,y+1,z+1,voxid,0)
                        ind = self.add_data(vertex_data,ind,e0,e3,e2,e0,e2,e1)
                    #bottom
                    if self.check_emp((x,y - 1,z),voxle_data):
                        e0 = (x,y,z,voxid,1)
                        e1 = (x+1,y,z,voxid,1)
                        e2 = (x+1,y,z+1,voxid,1)
                        e3 = (x,y+1,z+1,voxid,1)
                        ind = self.add_data(vertex_data,ind,e0,e2,e3,e0,e1,e2)                   
                    #right 
                    if self.check_emp((x+1,y,z),voxle_data):
                        e0 = (x+1,y,z,voxid,2)
                        e1 = (x+1,y+1,z,voxid,2)
                        e2 = (x+1,y+1,z+1,voxid,2)
                        e3 = (x+1,y,z+1,voxid,2)
                        ind = self.add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3)  
                    #left
                    if self.check_emp((x-1,y,z),voxle_data):
                        e0 = (x,y,z,voxid,3)
                        e1 = (x,y+1,z,voxid,3)
                        e2 = (x,y+1,z+1,voxid,3)
                        e3 = (x,y,z+1,voxid,3)
                        ind = self.add_data(vertex_data,ind,e0,e2,e1,e0,e3,e2) 
                    #back
                    if self.check_emp((x,y,z-1),voxle_data):
                        e0 = (x,y,z,voxid,4)
                        e1 = (x,y+1,z,voxid,4)
                        e2 = (x+1,y+1,z,voxid,4)
                        e3 = (x+1,y,z,voxid,4)
                        ind = self.add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3) 
                    #front
                    if self.check_emp((x,y,z+1),voxle_data):
                        e0 = (x,y,z+1,voxid,5)
                        e1 = (x,y+1,z+1,voxid,5)
                        e2 = (x+1,y+1,z+1,voxid,5)
                        e3 = (x+1,y,z+1,voxid,5)
                        ind = self.add_data(vertex_data,ind,e0,e2,e1,e0,e3,e2) 
        return vertex_data[:ind+1]
                      
    def check_emp(self,voxpos,voxel_data):
        x,y,z = voxpos
        if 0 <= x < self.chunk.chunk_size and 0 <= y < self.chunk.chunk_size and 0:
            if voxel_data[x + self.chunk.chunk_size * z + self.chunk.chunk_area * y]:
                return False 
        return True

    def vert_data(self)->np.array:
        mesh = self.chunk_mesh(self.chunk.b_voxel,self.vao.mine_form_size)
        return mesh

    def g_vbo(self):
        return self.app.ctx.buffer(self.vert_data())
