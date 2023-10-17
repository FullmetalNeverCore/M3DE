from numba import njit
import numpy as np
import moderngl as mgl
import pywavefront
from abc import ABC, abstractmethod
from components.chunk_config import *
from components.vao import * 
from components.vbo import *
from components.shad_prog import *
import pywavefront
from abc import ABC, abstractmethod
from components.txuring import *
import copy
import datetime 
import moderngl as mgl
import pygame
import moderngl_window as mglw
import time
from components.cam import *
import math 
from numba import njit
from components.noise import noise2,noise3

def add_data(vert_data, ind, *vertices):
    for vert in vertices:
        for a in vert:
            vert_data[ind] = a
            ind += 1
    return ind

def chunk_mesh(voxle_data,format_s):
        vertex_data = np.empty(chunk_vol*18*5*format_s,dtype='uint8')
        ind = 0 
        for x in range(chunk_size):
            for y in range(chunk_size):
                for z in range(chunk_size):
                    voxid = voxle_data[x+chunk_size*z+chunk_area*y]
                    if not voxid:
                        continue
                    #Cheking if side is visible to camera
                    #top of the block
                    if check_emp((x,y + 1,z),voxle_data):
                        e0 = (x,y+1,z,voxid,0)
                        e1 = (x+1,y+1,z,voxid,0)
                        e2 = (x+1,y+1,z+1,voxid,0)
                        e3 = (x,y+1,z+1,voxid,0)
                        ind = add_data(vertex_data,ind,e0,e3,e2,e0,e2,e1)
                    #bottom
                    if check_emp((x,y - 1,z),voxle_data):
                        e0 = (x,y,z,voxid,1)
                        e1 = (x+1,y,z,voxid,1)
                        e2 = (x+1,y,z+1,voxid,1)
                        e3 = (x,y,z+1,voxid,1)
                        ind = add_data(vertex_data,ind,e0,e2,e3,e0,e1,e2)                   
                    #right 
                    if check_emp((x+1,y,z),voxle_data):
                        e0 = (x+1,y,z,voxid,2)
                        e1 = (x+1,y+1,z,voxid,2)
                        e2 = (x+1,y+1,z+1,voxid,2)
                        e3 = (x+1,y,z+1,voxid,2)
                        ind = add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3)  
                    #left
                    if check_emp((x-1,y,z),voxle_data):
                        e0 = (x,y,z,voxid,3)
                        e1 = (x,y+1,z,voxid,3)
                        e2 = (x,y+1,z+1,voxid,3)
                        e3 = (x,y,z+1,voxid,3)
                        ind = add_data(vertex_data,ind,e0,e2,e1,e0,e3,e2) 
                    #back
                    if check_emp((x,y,z-1),voxle_data):
                        e0 = (x,y,z,voxid,4)
                        e1 = (x,y+1,z,voxid,4)
                        e2 = (x+1,y+1,z,voxid,4)
                        e3 = (x+1,y,z,voxid,4)
                        ind = add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3) 
                    #front
                    if check_emp((x,y,z+1),voxle_data):
                        e0 = (x,y,z+1,voxid,5)
                        e1 = (x,y+1,z+1,voxid,5)
                        e2 = (x+1,y+1,z+1,voxid,5)
                        e3 = (x+1,y,z+1,voxid,5)
                        ind = add_data(vertex_data,ind,e0,e2,e1,e0,e3,e2) 
        return vertex_data[:ind+1]

@staticmethod
@njit
def gen_terr(vox,zx,zy,zz):
        for x in range(chunk_size):
            wx = x + zx
            for z in range(chunk_size):
                wz = z + zz 
                world_hei = g_hei(wx,wz)
                local_hei = min(world_hei - zy,chunk_size)
                for y in range(local_hei):
                    wy = y + zy
                    vox[x+chunk_size*z+chunk_area*y] = wy + 1


@njit
def g_hei(x, z):
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - center_xz, z - center_xz), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = center_y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height,  noise2(x * f8, z * f8) + 2)
    height *= island

    return int(height)

def check_emp(voxpos,voxel_data):
        x,y,z = voxpos
        if 0 <= x < chunk_size and 0 <= y < chunk_size and 0 <= z < chunk_size:
            if voxel_data[x + chunk_size * z + chunk_area * y]:
                return False 
        return True