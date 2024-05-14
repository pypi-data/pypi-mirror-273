class Obj:
    def __init__(self, vao_name='cube', pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1), tex_id='test',
                 attached_script=""):
        self.vao = vao_name
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.tex_id = tex_id
        self.script = attached_script


if __name__ == '__main__':
    print("You are forbidden to be here...")
