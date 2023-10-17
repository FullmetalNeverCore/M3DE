import components.vao

class Mesh:
    def __init__(self,chunk):
        self.app = chunk.app
        self.chunk = chunk
        self.sp = chunk.sp
        self.gen_vao = chunk.vao
    
    def making_vao(self):
        return self.gen_vao.g_vao_special(sp=self.sp,ch=self.chunk)
    
    def render(self):
        self.making_vao().render()