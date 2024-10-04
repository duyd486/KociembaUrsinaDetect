from ursina import *
import random

app = Ursina()
class RubikCube(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        plane = Entity(model='quad', scale=60, texture='white_cube', texture_scale=(60, 60), rotation_x=90, y=-5,
               color=color.light_gray)
        sky = Entity(model='sphere', scale=150, texture='textures/test', double_sided=True)  # sky
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.load_game()


    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model='models/custom_cube', texture= 'textures/my_rubik_texture', position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity(model = 'models/custom_cube', texture = 'textures/dirt', position = (0,0,0))
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'UP': 'y', 'DOWN': 'y', 'FRONT': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'DOWN': self.DOWN, 'RIGHT': self.RIGHT, 'FRONT': self.FRONT,
                                    'BACK': self.BACK, 'UP': self.UP}
        self.animation_time = .2
        self.action_trigger = True
        print("load")


    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(90, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + 0.11)


    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0


    def create_cube_positions(self):
        self.LEFT = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.DOWN = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.FRONT = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.BACK = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.RIGHT = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.UP = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.LEFT | self.DOWN | self.FRONT | self.BACK | self.RIGHT | self.UP



    def input(self, key):
        if key == 'l' and self.action_trigger:
            self.rotate_side('LEFT')
        if key == 'd' and self.action_trigger:
            self.rotate_side('DOWN')
        if key == 'r' and self.action_trigger:
            self.rotate_side('RIGHT')
        if key == 'f' and self.action_trigger:
            self.rotate_side('FRONT')
        if key == 'b' and self.action_trigger:
            self.rotate_side('BACK')
        if key == 'u' and self.action_trigger:
            self.rotate_side('UP')





rubik = RubikCube()








app.run()