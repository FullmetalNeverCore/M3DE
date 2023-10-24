import numpy as np 
from components.vao import * 
from components.vbo import *
from components.shad_prog import *
import pygame as pg
import pywavefront
from abc import ABC, abstractmethod


class txuring:

    def __init__(self, app):
        # Setting the app as the context
        self.ctx = app
        # Setting the texture as the texture from texturing function
        self.tx = {0:self.texturing('./tx/dirt.jpg')
                   ,1:self.texturing('./tx/red.png')
                   ,2:self.texturing('./tx/Cat_diffuse.jpg'),
                   3:self.texturing('./tx/11133.jpg'),
                   4:self.texturing('./tx/noise.png'),
                   5:self.texturing('./tx/doom2.jpeg'),
                   6:self.use_tx_arr()}
        # Setting the skybox to the skybox from the skybox function
        self.sb = self.skybox('./tx/skybox/')

    # Defining the skybox function with the path argument
    def skybox(self, path):
        # Loading the textures for the skybox
        stx = [pg.image.load(f'{path}{x}.png') for x in ['right', 'left', 'top', 'bottom'] + ['front', 'back']]
        # Creating a texture cube
        box = self.ctx.texture_cube(stx[0].get_size(), 3, None)
        # Writing the texture data for each side of the cube
        for x in range(6):
            tx_data = pg.image.tostring(stx[x], 'RGB')
            box.write(x, tx_data)
        # Returning the box
        return box
    
    def use_tx_arr(self):
        tx = pg.image.load('./tx/tx_arr.png').convert()
        tx = pg.transform.flip(tx, flip_x=True, flip_y=False)
        layers = 3 * tx.get_height() // tx.get_width() #getting amount of layers
        return self.ctx.texture_array(size=(tx.get_width(),tx.get_height()//layers,layers),
        components=4,
        data=pg.image.tostring(tx,'RGBA'))

    # Defining the texturing function with path argument
    def texturing(self, path):
        # Loading the texture
        tx = pg.image.load(path).convert()
        # Flipping the texture vertically
        tx = pg.transform.flip(tx, flip_x=False, flip_y=True)
        # Creating a texture from the image data
        return self.ctx.texture(tx.get_size(), 3, pg.image.tostring(tx, 'RGB'))
