import glm
import pygame as pg

class Cam:
    def __init__(self,app):
        self.app = app
        self.position = glm.vec3(6,6,6) # position
        self.up = glm.vec3(0,2,0) # camera orientation
        self.forw = glm.vec3(0,0,-1)
        self.right = glm.vec3(1,0,0)
        #calculate aspect ratio of screen
        self.aspect_rat = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.view_matrix = self.get_v_matrix()
        self.proj_matrix = self.get_p_matrix()
    
    def update(self):
        self.move()
        self.view_matrix = self.get_v_matrix()

    def move(self):
        velo = 0.01 * self.app.delta_time # 0.01 speed
        if pg.key.get_pressed()[pg.K_w]:
            self.position += self.forw * velo
        if pg.key.get_pressed()[pg.K_s]:
            self.position -= self.forw * velo
        if pg.key.get_pressed()[pg.K_a]:
            self.position -= self.right * velo
        if pg.key.get_pressed()[pg.K_d]:
            self.position += self.right * velo
        if pg.key.get_pressed()[pg.K_q]:
            self.position += self.up * velo
        if pg.key.get_pressed()[pg.K_e]:
            self.position -= self.up * velo

    def get_v_matrix(self):
        return glm.lookAt(self.position,self.position + self.forw,self.up) # glm.vec3 - center of camera

    def get_p_matrix(self):
        return glm.perspective(glm.radians(50),self.aspect_rat,0.1,100) # 50 - FOV,how close it can get - 0.1,how far - 100 
