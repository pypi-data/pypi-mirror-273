from RenderCat.vbo import VBO
from RenderCat.shader_program import ShaderProgram


class VAO:
    # noinspection PyDictCreation
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}
        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.shaders['default'],
            vbo=self.vbo.vbos['cube'])
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.shaders['shadow_map'],
            vbo=self.vbo.vbos['cube'])
        self.vaos['overlay'] = self.get_vao(
            program=self.program.shaders['overlay'],
            vbo=self.vbo.vbos['overlay']
        )
        vaos_to_load = []
        try:
            with open(file="object_list.txt", mode='r') as vaolist:
                for line in vaolist:
                    value = line.split("|")
                    vaos_to_load.append([obj.rstrip() for obj in value])
                vaolist.close()
            vaolist.close()
        except PermissionError:
            raise Exception("Cannot open VBO list file: no permission.")
        except FileNotFoundError:
            raise Exception("VBO list not found!")
        for value in vaos_to_load:
            self.vaos[value[0]] = self.get_vao(
                program=self.program.shaders[value[2]],
                vbo=self.vbo.vbos[value[0]])
            self.vaos["shadow_" + value[0]] = self.get_vao(
                program=self.program.shaders['shadow_map'],
                vbo=self.vbo.vbos[value[0]])
        self.vaos['skybox'] = self.get_vao(
            program=self.program.shaders['skybox'],
            vbo=self.vbo.vbos['skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()


if __name__ == '__main__':
    print("You are forbidden to be here...")
