import numpy as np 
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
from components.perlin import *
import components.raycast





class Raycasting:

  @njit(fastmath=True)
  def raycasting(screen,mheight,mwidth,hmap,cmap,pos,angle,height,pitch,
  scrwidth,scrheight,delta_angle,ray_dist,fov,sheight)->'Screen Array':

        screen[:] = np.array([0,0,0])
        y_buff =  np.full(scrwidth,scrheight) #fill vertival lines with color 

        ray_ang = angle - fov #angle of first ray

        for nrays in range(scrwidth):
            sin_a = math.sin(ray_ang)
            cos_a = math.cos(ray_ang)
            
            for depth in range(1,ray_dist):
                x = int(pos[0] + depth * cos_a)

                if 0 < x < mwidth:
                    y = int(pos[1] + depth * sin_a)

                    if 0 < y < mheight:
                        depth *= math.cos(angle - ray_ang)
                        height_o_s = int((height - hmap[x,y][0])/ depth * sheight + pitch)
                        if not height_o_s > 0:height_o_s=0 
                        #draw v lines 
                        #scry - vertical y lines on screen 

                        if height_o_s < y_buff[nrays]:

                            for scry in range(height_o_s,y_buff[nrays]):
                                screen[nrays,scry] = cmap[x,y]

                            y_buff[nrays] = height_o_s

            ray_ang += delta_angle
        return screen 