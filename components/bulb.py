import pygame as pg
import numpy as np
import glm 

class Bulb:
    def __init__(self,pos=(3,3,-3),color=(1,1,1)):
        # Convert the color and position values to glm vectors
        self.clr = glm.vec3(color)
        self.pos = glm.vec3(pos)

        # Define Phong coefficients for the light source
        self.amb = 0.1 * self.clr  # ambient coefficient
        self.diffus = 0.8 * self.clr # diffusion coefficient
        self.spec = 1.0 * self.clr # specular coefficient
