from txuring import *
from vao import * 



class Gather:
    def __init__(self,app) -> None:
        self.app = app 
        self.tx = txuring(self.app.ctx)
        self.vao = general_VAO(self.app)

    def destroy(self):
        self.vao.destroy()