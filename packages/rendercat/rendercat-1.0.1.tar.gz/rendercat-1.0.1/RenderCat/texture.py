import pygame as pg
import moderngl as mgl


class Texture:
    # noinspection PyDictCreation
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        textures_to_load = []
        try:
            with open(file="texture_list.txt", mode='r') as texlist:
                for line in texlist:
                    value = line.split("|")
                    textures_to_load.append([tex.rstrip() for tex in value])
        except PermissionError:
            raise Exception("Cannot open texture list file: no permission.")
        except FileNotFoundError:
            raise Exception("texture list not found!")
        for texture in textures_to_load:
            if texture[0] == 'skybox':
                self.textures['skybox'] = self.get_texture_cube(dir_path=f"textures/{texture[1]}/", ext=texture[2])
            else:
                self.textures[texture[0]] = self.get_texture('textures/' + texture[1])
        self.textures['depth_texture'] = self.get_depth_texture()

    def get_depth_texture(self):
        depth_texture = self.ctx.depth_texture((self.app.WIN_SIZE[0] * 2, self.app.WIN_SIZE[1] * 2))
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))

        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]


if __name__ == '__main__':
    print("You are forbidden to be here...")
