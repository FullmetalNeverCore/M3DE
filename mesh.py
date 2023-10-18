import components.vao

class Mesh:
    def __init__(self,chunk):
        self.app = chunk.app
        self.chunk = chunk
        self.sp = chunk.sp
        self.gen_vao = chunk.vao.g_vao_special(sp=self.sp,ch=self.chunk)
    
    def render(self):
        self.gen_vao.render()