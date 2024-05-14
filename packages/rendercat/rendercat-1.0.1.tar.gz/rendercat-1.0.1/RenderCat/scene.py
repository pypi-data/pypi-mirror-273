from RenderCat.loadobject import Obj
from RenderCat.model import *


class Scene:
    def __init__(self, app, mapname="main"):
        self.app = app
        self.objects = []
        self.load(mapname)
        self.skybox = Skybox(app)

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self, map_to_load):
        app = self.app
        add = self.add_object
        objbuffer = []
        try:
            with open(file=f"Scenes/{map_to_load}.rcs", mode='r') as mapfile:
                for line in mapfile:
                    value = line.split("|")
                    rawvalue = value[1].split(',')
                    pos = glm.vec3(float(rawvalue[0]), float(rawvalue[1]), float(rawvalue[2]))
                    rawvalue = value[2].split(',')
                    rot = glm.vec3(glm.radians(float(rawvalue[0])), glm.radians(float(rawvalue[1])), glm.radians(float(rawvalue[2])))
                    rawvalue = value[3].split(',')
                    scale = glm.vec3(float(rawvalue[0]), float(rawvalue[1]), float(rawvalue[2]))
                    objbuffer.append(Obj(vao_name=value[0], pos=pos, rot=rot, scale=scale,
                                         tex_id=value[4].rstrip(), attached_script=value[5].rstrip()))
                mapfile.close()
            mapfile.close()
        except PermissionError:
            raise Exception("Cannot open map_to_load file: no permission.")
        except FileNotFoundError:
            raise Exception("Map not found!")
        for i in objbuffer:
            if i.script != 'None':
                with open(file=f"Scenes/{map_to_load}/{i.script}.py") as scr:
                    src = scr.read()
            else:
                src = ''
            add(ExtendedBaseModel(app, pos=i.pos, rot=i.rot, scale=i.scale, tex_id=i.tex_id, vao_name=i.vao,
                                  attachment=src))

    def update(self):
        pass

    def render(self):
        self.app.ctx.screen.use()
        for obj in self.objects:
            obj.render()
        self.skybox.render()


if __name__ == '__main__':
    print("You are forbidden to be here...")
