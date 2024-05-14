import sys
import moderngl as mgl
import pygame as pg
from RenderCat.camera import Camera
from RenderCat.light import Light
from RenderCat.mesh import Mesh
from RenderCat.scene import Scene
from RenderCat.scene_renderer import SceneRenderer


class Engine:
    def __init__(self, win_size=None):
        pg.init()
        if win_size is not None:
            self.WIN_SIZE = win_size
        else:
            self.WIN_SIZE = pg.display.get_desktop_sizes()[0]
        self.window = pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF | pg.NOFRAME)
        pg.event.set_grab(False)
        pg.mouse.set_visible(False)
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST)
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        self.light = Light(position=(15, 15, -3))
        self.camera = Camera(self, position=(0, 5, 15))
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.scene_renderer = SceneRenderer(self)
        self.screen = pg.Surface(self.WIN_SIZE)
        self.overlay = self.mesh.vao.vaos['overlay']
        self.overlay.program['u_resolution'] = self.WIN_SIZE

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.mesh.destroy()
                self.scene_renderer.destroy()
                sys.exit()

    def render(self):
        self.screen.fill((100, 200, 15))
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        self.tick()
        self.scene_renderer.render()
        texture = self.screen.convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=self.WIN_SIZE, components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        texture.repeat_x = False
        texture.repeat_y = False
        self.overlay.program['u_texture_0'] = 1
        texture.use(location=1)
        self.overlay.render()
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.render()
            self.delta_time = self.clock.tick(60)

    def tick(self):
        pg.draw.circle(self.screen, (0, 0, 0), (self.WIN_SIZE[0] // 2, self.WIN_SIZE[1] // 2), 10)
        dx, dy = pg.mouse.get_rel()
        pg.mouse.set_pos((self.WIN_SIZE[0] / 2, self.WIN_SIZE[1] / 2))
        self.camera.rotate(dx, dy)
        self.camera.move()


print("RenderCat v.1")
