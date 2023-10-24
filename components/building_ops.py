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
from numba import uint8


@njit
def add_data(vert_data, ind, *vertices):
    for vert in vertices:
            vert_data[ind] = vert
            ind += 1
    return ind

#Ambient Occlusion
@njit 
def ambient_occlusion(locpos,wrldpos,wrldvox,direction):
    x,y,z = locpos 
    xx,xy,xz = wrldpos
    match direction:
        case 'Y':
            a = check_emp((x    , y, z - 1), (xx    , xy, xz - 1), wrldvox)
            b = check_emp((x - 1, y, z - 1), (xx - 1, xy, xz - 1), wrldvox)
            c = check_emp((x - 1, y, z    ), (xx - 1, xy, xz    ), wrldvox)
            d = check_emp((x - 1, y, z + 1), (xx - 1, xy, xz + 1), wrldvox)
            e = check_emp((x    , y, z + 1), (xx    , xy, xz + 1), wrldvox)
            f = check_emp((x + 1, y, z + 1), (xx + 1, xy, xz + 1), wrldvox)
            g = check_emp((x + 1, y, z    ), (xx + 1, xy, xz    ), wrldvox)
            h = check_emp((x + 1, y, z - 1), (xx + 1, xy, xz - 1), wrldvox)
        case 'X':
            a = check_emp((x, y    , z - 1), (xx, xy    , xz - 1), wrldvox)
            b = check_emp((x, y - 1, z - 1), (xx, xy - 1, xz - 1), wrldvox)
            c = check_emp((x, y - 1, z    ), (xx, xy - 1, xz    ), wrldvox)
            d = check_emp((x, y - 1, z + 1), (xx, xy - 1, xz + 1), wrldvox)
            e = check_emp((x, y    , z + 1), (xx, xy    , xz + 1), wrldvox)
            f = check_emp((x, y + 1, z + 1), (xx, xy + 1, xz + 1), wrldvox)
            g = check_emp((x, y + 1, z    ), (xx, xy + 1, xz    ), wrldvox)
            h = check_emp((x, y + 1, z - 1), (xx, xy + 1, xz - 1), wrldvox)          
        case 'Z':
            a = check_emp((x - 1, y    , z), (xx - 1, xy    , xz), wrldvox)
            b = check_emp((x - 1, y - 1, z), (xx - 1, xy - 1, xz), wrldvox)
            c = check_emp((x    , y - 1, z), (xx    , xy - 1, xz), wrldvox)
            d = check_emp((x + 1, y - 1, z), (xx + 1, xy - 1, xz), wrldvox)
            e = check_emp((x + 1, y    , z), (xx + 1, xy    , xz), wrldvox)
            f = check_emp((x + 1, y + 1, z), (xx + 1, xy + 1, xz), wrldvox)
            g = check_emp((x    , y + 1, z), (xx    , xy + 1, xz), wrldvox)
            h = check_emp((x - 1, y + 1, z), (xx - 1, xy + 1, xz), wrldvox)             
    return (a+b+c),(g+h+a),(e+f+g),(c+d+e)
    
    

@njit
def convert_to_uint(x,y,z,voxid,id,amb,dirid):
    #making bitwise shift for optimisation 
    bbit,cbit,dbit,ebit,fbit,gbit = 6,6,8,3,2,1
    fgbit = fbit + gbit 
    efgbit = ebit + fgbit 
    defgbit = dbit + efgbit
    cdefgbit = cbit + defgbit
    bcdefgbit = bbit + cdefgbit
    return (x<<bcdefgbit|y<<cdefgbit|z<<defgbit|voxid<<efgbit|id<<fgbit|amb<<gbit|dirid)
@njit
def chunk_mesh(voxle_data,format_s,ch_position,wrld_vox):
        vertex_data = np.empty(chunk_vol*18*5*format_s,dtype='uint32')
        ind = 0 
        for x in range(chunk_size):
            for y in range(chunk_size):
                for z in range(chunk_size):
                    voxid = voxle_data[x+chunk_size*z+chunk_area*y]
                    if not voxid:
                        continue
                    
                    #checking voxel positions in world
                    wx,wy,wz = ch_position
                    xx = x + wx * chunk_size
                    xy = y + wy * chunk_size
                    xz = z + wz * chunk_size
                    #Cheking if side is visible to camera
                    #top of the block

                    if check_emp((x,y + 1,z),(xx,xy + 1,xz), wrld_vox):
                        amb = ambient_occlusion((x,y + 1,z),(xx,xy + 1,xz), wrld_vox,direction='Y')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x,y+1,z,voxid,0,amb[0],dir_id)
                        e1 = convert_to_uint(x+1,y+1,z,voxid,0,amb[1],dir_id)
                        e2 = convert_to_uint(x+1,y+1,z+1,voxid,0,amb[2],dir_id)
                        e3 = convert_to_uint(x,y+1,z+1,voxid,0,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e1,e0,e3,e1,e3,e2)
                        else:
                            ind = add_data(vertex_data,ind,e0,e3,e2,e0,e2,e1)
                    #bottom
                    if check_emp((x,y - 1,z),(xx,xy - 1,xz), wrld_vox):
                        amb = ambient_occlusion((x,y - 1,z),(xx,xy - 1,xz), wrld_vox,direction='Y')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x,y,z,voxid,1,amb[0],dir_id)
                        e1 = convert_to_uint(x+1,y,z,voxid,1,amb[1],dir_id)
                        e2 = convert_to_uint(x+1,y,z+1,voxid,1,amb[2],dir_id)
                        e3 = convert_to_uint(x,y,z+1,voxid,1,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e1,e3,e0,e1,e2,e3)
                        else:
                            ind = add_data(vertex_data,ind,e0,e2,e3,e0,e1,e2)                  
                    #right 
                    if check_emp((x+1,y,z),(xx+1,xy,xz), wrld_vox):
                        amb = ambient_occlusion((x+1,y,z),(xx+1,xy,xz), wrld_vox,direction='X')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x+1,y,z,voxid,2,amb[0],dir_id)
                        e1 = convert_to_uint(x+1,y+1,z,voxid,2,amb[1],dir_id)
                        e2 = convert_to_uint(x+1,y+1,z+1,voxid,2,amb[2],dir_id)
                        e3 = convert_to_uint(x+1,y,z+1,voxid,2,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e3,e0,e1,e3,e1,e2)  
                        else:
                            ind = add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3)  
                    #left
                    if check_emp((x-1,y,z),(xx-1,xy,xz), wrld_vox):
                        amb = ambient_occlusion((x-1,y,z),(xx-1,xy,xz), wrld_vox,direction='X')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x,y,z,voxid,3,amb[0],dir_id)
                        e1 = convert_to_uint(x,y+1,z,voxid,3,amb[1],dir_id)
                        e2 = convert_to_uint(x,y+1,z+1,voxid,3,amb[2],dir_id)
                        e3 = convert_to_uint(x,y,z+1,voxid,3,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e3,e1,e0,e3,e2,e1)
                        else:
                            ind = add_data(vertex_data,ind,e0,e2,e1,e0,e3,e2) 
                    #back
                    if check_emp((x,y,z-1),(xx,xy,xz-1), wrld_vox):
                        amb = ambient_occlusion((x,y,z-1),(xx,xy,xz-1), wrld_vox,direction='Z')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x,y,z,voxid,4,amb[0],dir_id)
                        e1 = convert_to_uint(x,y+1,z,voxid,4,amb[1],dir_id)
                        e2 = convert_to_uint(x+1,y+1,z,voxid,4,amb[2],dir_id)
                        e3 = convert_to_uint(x+1,y,z,voxid,4,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e3,e0,e1,e3,e1,e2)
                        else:
                            ind = add_data(vertex_data,ind,e0,e1,e2,e0,e2,e3) 
                    #front
                    if check_emp((x,y,z+1),(xx,xy,xz+1), wrld_vox):
                        amb = ambient_occlusion((x,y,z+1),(xx,xy,xz+1), wrld_vox,direction='Z')
                        dir_id = amb[1] + amb[3] > amb[0] + amb[2]
                        e0 = convert_to_uint(x,y,z+1,voxid,5,amb[0],dir_id)
                        e1 = convert_to_uint(x,y+1,z+1,voxid,5,amb[1],dir_id)
                        e2 = convert_to_uint(x+1,y+1,z+1,voxid,5,amb[2],dir_id)
                        e3 = convert_to_uint(x+1,y,z+1,voxid,5,amb[3],dir_id)
                        if dir_id:
                            ind = add_data(vertex_data,ind,e3,e1,e0,e3,e2,e1)
                        else:
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
                    vox[x+chunk_size*z+chunk_area*y] = 2 #texture id


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


#get chunk position
@njit
def get_ch_ind(w_vox_pos)->'Chunk Index':
    wx,wy,wz = w_vox_pos
    cx = wx // chunk_size
    cy = wy // chunk_size
    cz = wz // chunk_size
    if not (0 <= cx < world_wid and 0 <= cy < world_hei and 0 <= cz < world_dim):
        return -1 # if coords of chunks is after the world limit return -1
    index = cx + world_wid * cz + world_area * cy 
    return index
    
@njit
def check_emp(voxpos,w_vox_pos,wrld_vox)->bool:
    ch_ind = get_ch_ind(w_vox_pos)
    if ch_ind < -1:
        return False
    #if here then chunk is within the world limit
    ch_vox = wrld_vox[ch_ind]
    x,y,z = voxpos 
    vox_ind = x % chunk_size + z % chunk_size * chunk_size + y % chunk_size * chunk_area
    if ch_vox[vox_ind]:
        return False
    return True