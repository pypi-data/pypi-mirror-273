import glm
import math


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos=glm.vec3(0, 0, 0), rot=glm.vec3(0, 0, 0), scale=glm.vec3(1, 1, 1)):
        self.vao_name = vao_name
        self.app = app
        self.pos = pos
        self.rot = rot
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        rot = list(self.rot)
        for i in range(0, 2):
            rot[i] = rot[i] / 180 * math.pi
        m_model = glm.mat4(1.0)
        m_model = glm.translate(m_model, self.pos)
        m_model = glm.rotate(m_model, rot[0], glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, rot[1], glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, rot[2], glm.vec3(0, 0, 1))
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


# noinspection PyAttributeOutsideInit
class ExtendedBaseModel(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos, rot, scale, attachment=''):
        self.script = attachment
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        pos, rot, scale = self.pos, self.rot, self.scale
        print()
        exec(self.script)
        pos, rot, scale = self.pos, self.rot, self.scale
        m_model = glm.mat4(1.0)
        m_model = glm.translate(m_model, pos)
        m_model = glm.rotate(m_model, rot[0], glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, rot[1], glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, rot[2], glm.vec3(0, 0, 1))
        m_model = glm.scale(m_model, scale)
        self.pos, self.rot, self.scale = pos, rot, scale
        self.m_model = m_model
        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    # noinspection PyAttributeOutsideInit
    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        # resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)
        # shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # mvp
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    def __init__(self, app, vao_name='cube', tex_id=1, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class Skybox(BaseModel):
    def __init__(self, app):
        super().__init__(app, 'skybox', 'skybox', (0, 0, 0), (0, 0, 0), (1, 1, 1))
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.on_init()

    def update(self):
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        # texture
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
