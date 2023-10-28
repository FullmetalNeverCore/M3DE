from components.txuring import *
from components.vao import * 
from components.wrld import * 


class Gather:
    def __init__(self,app) -> None:
        self.app = app 
        self.tx = txuring(self.app.ctx)
        self.vao = general_VAO(self.app)
        self.sp = self.vao.sp
        self.minesp = self.sp.obj['mine'] 
        if not self.app.status == 'benchmark':self.world = World(self.app,self.minesp,self.vao)

    def destroy(self):
        self.vao.destroy()