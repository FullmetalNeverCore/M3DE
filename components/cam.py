import glm
import pygame as pg
import numpy as np
import math 

class Cam:
    def __init__(self, app,dist=35)->None:
        self.app = app
        # calculate aspect ratio of screen
        self.aspect_rat = app.WIN_SIZE[0] / app.WIN_SIZE[1] # gets aspect ratio of screen
        self.position = glm.vec3(0, 0, 0) # sets initial position of camera
        self.up = glm.vec3(0, 2, 0) # sets camera's up direction
        self.forw = glm.vec3(0, 0, -1) # sets camera's forward direction
        self.right = glm.vec3(1, 0, 0) # sets camera's right direction
        self.vertical_ax = -90 # sets vertical axis for camera
        self.horiz_ax = 0 # sets horizontal axis for camera
        self.fov = 100
        self.near_distance = 0.1  # Near plane distance
        self.far_distance = float(dist)

        #raycasting
        self.rfov = math.pi/2 #raycasting fov
        self.rhfov = self.rfov / 2 # raycasting height fov
        self.campos = np.array([0,0],dtype=float)
        self.camheight = 270
        self.campitch = 40
        self.cam_angle = math.pi/4
        self.nrays = self.app.WIN_SIZE[0]
        self.delta_angle = self.rfov /self.nrays
        self.ray_dist = 2000
        self.scale = 900
        self.screen_array = np.full((self.app.WIN_SIZE[0],self.app.WIN_SIZE[1],3),(0,0,0))
        
        #raycasting control 
        self.ang_v = 0.1
        self.vel = 6
        
        # #Minecraft own settings - for test
        # self.vertic_fov = glm.radians(50)
        # self.horiz_fov = 2 * math.atan(math.tan(self.vertic_fov*0.5)*self.aspect_rat)
        # self.far = 1000.0
        # self.near = 0.5
        # self.pitch = glm.radians(89)#89deg * pi/180 deg to rad
        # self.plr_obj_spd = 0.05
        # self.plr_obj_rot_spd = 0.03
        # self.mouse_sens = 0.02

        # #Minecraft perscpectives

        # self.yaw = glm.radians(yaw)
        # self.mine_m_proj = glm.perspective(self.vertic_fov,self.aspect_rat,self.near,self.far)
        # self.mine_m_view = glm.mat4()

        if self.app.uogl == 'y':
            self.view_matrix = self.get_v_matrix() # gets the view matrix for the camera
            self.proj_matrix = self.get_p_matrix() # gets the projection matrix for the camera


    def ray_move(self)->None:
        sina = math.sin(self.cam_angle)
        cosa = math.cos(self.cam_angle)

        #Cam control for raycasting engine6

        if pg.key.get_pressed()[pg.K_UP]:
            self.campitch += self.vel
        if pg.key.get_pressed()[pg.K_DOWN]:
            self.campitch -= self.vel
        if pg.key.get_pressed()[pg.K_LEFT]:
            self.cam_angle -= self.ang_v
        if pg.key.get_pressed()[pg.K_RIGHT]:
            self.cam_angle += self.ang_v

        if pg.key.get_pressed()[pg.K_w]:
            self.campos[0] += self.vel * cosa 
            self.campos[1] += self.vel * sina
        if pg.key.get_pressed()[pg.K_s]:
            self.campos[0] -= self.vel * cosa 
            self.campos[1] -= self.vel * sina
        if pg.key.get_pressed()[pg.K_a]:
            self.campos[0] -= self.vel * cosa 
            self.campos[1] += self.vel * sina
        if pg.key.get_pressed()[pg.K_d]:
            self.campos[0] += self.vel * cosa 
            self.campos[1] -= self.vel * sina
        


    def rotate(self)->None:
        rel_x, rel_y = pg.mouse.get_rel() # gets relative position of the mouse
        self.vertical_ax += rel_x * 0.04 # adjusts the vertical axis of the camera based on mouse movement
        self.horiz_ax -= rel_y * 0.04 # adjusts the horizontal axis of the camera based on mouse movement
        self.horiz_ax = max(-89, min(89, self.horiz_ax)) # keeps the camera within a certain range of vertical motion

    def update_camera_vectors(self)->None:
        vertic, horiz = glm.radians(self.vertical_ax), glm.radians(self.horiz_ax) # converts the vertical and horizontal axes to radians
        
        # calculates the forward direction of the camera based on the vertical and horizontal axes
        self.forw.x = glm.cos(vertic) * glm.cos(horiz)
        self.forw.y = glm.sin(horiz)
        self.forw.z = glm.sin(vertic) * glm.cos(horiz)

        self.forward = glm.normalize(self.forw) # normalizes the forward direction vector
        self.right = glm.normalize(glm.cross(self.forw, glm.vec3(0, 1, 0))) # calculates the right direction of the camera
        self.up = glm.normalize(glm.cross(self.right, self.forw)) # calculates the up direction of the camera
    
    def update(self)->None:
        if not self.app.uogl == 'y':
            self.ray_move()
        else:
            self.move()
            # updates camera position based on user input
            self.rotate() 
            # updates camera rotation based on user input
            self.update_camera_vectors() 
            # updates camera vectors based on current rotation
            self.view_matrix = self.get_v_matrix() 
        #print(self.view_matrix)
        #print(self.proj_matrix)
        # updates the view matrix based on the camera's current position and orientation

    def move(self)->None:
        velo = 0.005 * self.app.d_time # 0.01 speed
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

    def get_v_matrix(self)->None:
        return glm.lookAt(self.position,self.position + self.forw,self.up) 

    def get_p_matrix(self)->None:
        projection_matrix = np.array([
            [1 / (self.aspect_rat * np.tan(np.radians(self.fov / 2))), 0, 0, 0],
            [0, 1 / np.tan(np.radians(self.fov / 2)), 0, 0],
            [0, 0, -(self.far_distance + self.near_distance) / (self.far_distance - self.near_distance), -1],
            [0, 0, -(2 * self.far_distance * self.near_distance) / (self.far_distance - self.near_distance), 0]
        ], dtype=np.float32)
        return projection_matrix
    
