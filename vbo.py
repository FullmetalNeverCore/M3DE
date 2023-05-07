import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod



class VBO_interface(ABC):
    

    @abstractmethod
    def vert_data(self):
        raise NotImplementedError
    
    @abstractmethod
    def destroy(self):
        raise NotImplementedError

    @abstractmethod
    def g_vbo(self):
        raise NotImplementedError
    
class tri_VBO(VBO_interface):

    def __init__(self,app):
        self.app = app 
        self.vbo = self.g_vbo()

    def destroy(self):
        self.vbo.release()

    def vert_data(self) -> list:
        vert_data = [(-0.6,-0.8,0.0),(0.6,-0.8,0.0),(0.0,0.8,0.0)]
        #f4 float32
        vert_data = np.array(vert_data,dtype='f4')
        return vert_data

    def g_vbo(self):
        #vbo - vertex buffer obj
        vert_data = self.vert_data()
        vbo = self.app.ctx.buffer(vert_data)
        return vbo
    
class cube_VBO(VBO_interface):
    def __init__(self,app):
        self.app = app 
        self.vbo = self.g_vbo()

    def destroy(self):
        self.vbo.release()
    
    @staticmethod
    def g_data(vert,ind):
        return np.array([vert[i] for tri in ind for i in tri],dtype='f4')

    def vert_data(self) -> list:
        vert_data = [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1),
                     (-1,1,-1),(-1,-1,-1),(1,-1,-1),(1,1,-1)]
        
        ind = [(0,2,3),(0,1,2),
               (1,7,2),(1,6,7),
               (6,5,4),(4,7,6),
               (3,4,5),(3,5,0),
               (3,7,4),(3,2,7),
               (0,6,1),(0,5,6)]
        
        tx_coord = [(0,0),(1,0),(1,1),(0,1)]
        tx_coord_ind = [(0,2,3),(0,1,2),
                        (0,2,3),(0,1,2),
                        (0,1,2),(2,3,0),
                        (2,3,0),(2,0,1),
                        (0,2,3),(0,1,2),
                        (3,1,2),(3,0,1),
                        ]
        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        
        normals = np.array(normals, dtype='f4').reshape(36, 3)
        geom_data = self.g_data(vert_data,ind)
        tex_data = self.g_data(tx_coord,tx_coord_ind)

        geom_data = np.hstack([normals,geom_data])
        geom_data = np.hstack([tex_data,geom_data])

        return geom_data

    def g_vbo(self):
        #vbo - vertex buffer obj
        vert_data = self.vert_data()
        vbo = self.app.ctx.buffer(vert_data)
        return vbo

class twins_VBO(VBO_interface):

    def __init__(self,app):
        self.app = app 
        self.vbo = self.g_vbo()



    def vert_data(self):
        objs = pywavefront.Wavefront('./model/model.obj', cache=True, parse=True)
        print(objs)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data



    def destroy(self):
        self.vbo.release()


    def g_vbo(self):
        #vbo - vertex buffer obj
        vert_data = self.vert_data()
        vbo = self.app.ctx.buffer(vert_data)
        return vbo

