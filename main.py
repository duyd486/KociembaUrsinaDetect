
from ursina import *
from solve_2d_cube import *
import cv2
from ursina.color import text_color
import random

app = Ursina(title='DUY DEP TRAI',icon='textures/my_dog_icon.ico')
class RubikCube(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        plane = Entity(model='quad', scale=40, texture='textures/grass.jpg', texture_scale=(60, 60), rotation_x=90, y=-5)
        sky = Entity(model='cube', scale=150, texture='textures/test', double_sided=True)  # sky
        window.borderless = False
        EditorCamera()
        camera.world_position = (0, 0, -20)

        # self.text = TextField(scale = 0.1, line_height= 1.1, character_limit=None)
        # self.text.text = dedent("Hello")
        # self.text.render()

        self.message = Text(origin=(0,18))
        self.message.text = dedent("Sử dụng URLFDB để di chuyển khối rubik, ấn O để mở camera, I để giải từng bước, S để xáo").strip()

        self.my_step = Text(origin=(0,-14), scale_override = 3)
        #self.my_step.size = 0.5
        self.my_step.text = dedent("Hi!")

        #cv2 code
        self.solution = ""
        self.speed_up_move = 0
        self.normal_move = 0.5
        self.delay_move = 0.08
        self.step = 0
        self.firstCall = True
        self.myvalues = ""
        self.re_conv = {
            # "F" : "F'",
            # "F'" : "F",
            # "F2" : "F2",
            # "R" : "R'",
            # "R2" : "R2",
            # "R'" : "R",
            # "B" : "B'",
            # "B2" : "B2",
            # "B'" : "B",
            # "L" : "L'",
            # "L2" : "L2",
            # "L'" : "L",
            # "U" : "U'",
            # "U2" : "U2",
            # "U'" : "U",
            # "D" : "D'",
            # "D2" : "D2",
            # "D'" : "D",
            "F": "f'",
            "F'": "f",
            "F2": "f2",
            "R": "r'",
            "R2": "r2",
            "R'": "r",
            "B": "b'",
            "B2": "b2",
            "B'": "b",
            "L": "l'",
            "L2": "l2",
            "L'": "l",
            "U": "u'",
            "U2": "u2",
            "U'": "u",
            "D": "d'",
            "D2": "d2",
            "D'": "d",
        }
        self.state = {
            'up': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', ],
            'right': ['white', 'white', 'white', 'white', 'red', 'white', 'white', 'white', 'white', ],
            'front': ['white', 'white', 'white', 'white', 'green', 'white', 'white', 'white', 'white', ],
            'down': ['white', 'white', 'white', 'white', 'yellow', 'white', 'white', 'white', 'white', ],
            'left': ['white', 'white', 'white', 'white', 'orange', 'white', 'white', 'white', 'white', ],
            'back': ['white', 'white', 'white', 'white', 'blue', 'white', 'white', 'white', 'white', ]
        }
        self.stickers = {
            'main': [
                [200, 120], [300, 120], [400, 120],
                [200, 220], [300, 220], [400, 220],
                [200, 320], [300, 320], [400, 320]
            ],
            'current': [
                [20, 20], [54, 20], [88, 20],
                [20, 54], [54, 54], [88, 54],
                [20, 88], [54, 88], [88, 88]
            ],
            'preview': [
                [20, 130], [54, 130], [88, 130],
                [20, 164], [54, 164], [88, 164],
                [20, 198], [54, 198], [88, 198]
            ],
            'left': [
                [50, 280], [94, 280], [138, 280],
                [50, 324], [94, 324], [138, 324],
                [50, 368], [94, 368], [138, 368]
            ],
            'front': [
                [188, 280], [232, 280], [276, 280],
                [188, 324], [232, 324], [276, 324],
                [188, 368], [232, 368], [276, 368]
            ],
            'right': [
                [326, 280], [370, 280], [414, 280],
                [326, 324], [370, 324], [414, 324],
                [326, 368], [370, 368], [414, 368]
            ],
            'up': [
                [188, 128], [232, 128], [276, 128],
                [188, 172], [232, 172], [276, 172],
                [188, 216], [232, 216], [276, 216]
            ],
            'down': [
                [188, 434], [232, 434], [276, 434],
                [188, 478], [232, 478], [276, 478],
                [188, 522], [232, 522], [276, 522]
            ],
            'back': [
                [464, 280], [508, 280], [552, 280],
                [464, 324], [508, 324], [552, 324],
                [464, 368], [508, 368], [552, 368]
            ],
        }
        self.check_state = []
        self.solved = False

        self.load_game()

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model='models/custom_cube', texture= 'textures/my_rubik_texture', position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity(model = 'models/custom_cube', texture = 'textures/dirt', position = (0,0,0))
        self.rotation_axes = {'LEFT': 'x', 'RIGHT': 'x', 'UP': 'y', 'DOWN': 'y', 'FRONT': 'z', 'BACK': 'z'}
        self.cubes_side_positons = {'LEFT': self.LEFT, 'DOWN': self.DOWN, 'RIGHT': self.RIGHT, 'FRONT': self.FRONT,
                                    'BACK': self.BACK, 'UP': self.UP}
        self.animation_time = 0.2
        self.action_trigger = True
        print("load")


    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name, degree):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                eval(f'self.PARENT.animate_rotation_{rotation_axis}(degree, duration=self.animation_time)')
        invoke(self.toggle_animation_trigger, delay=self.animation_time + self.delay_move)

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


    def scramble(self):
        print("scram")
        possible_move = ['l','r','u','d','b','f']
        self.speed_up_move = 0
        for i in range(25):
            self.move(random.choice(possible_move))
        self.speed_up_move = self.normal_move
        self.my_step.text = dedent("Scamble done!")

    def rubik_detect(self):
        print("Hi im rubik detect")
        print("Wait a second")

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        while True:
            hsv=[]
            current_state=[]
            ret,img=cap.read()
            #img=cv2.flip(img,1)
            frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            mask = np.zeros(frame.shape, dtype=np.uint8)

            draw_stickers(img,self.stickers,'main')
            draw_stickers(img,self.stickers,'current')
            draw_preview_stickers(preview,self.stickers)
            fill_stickers(preview,self.stickers,self.state)
            texton_preview_stickers(preview,self.stickers)
            for i in range(9):
                hsv.append(frame[self.stickers['main'][i][1]+10][self.stickers['main'][i][0]+10])

            a=0
            for x,y in self.stickers['current']:
                color_name=color_detect(hsv[a][0],hsv[a][1],hsv[a][2])
                cv2.rectangle(img,(x,y),(x+30,y+30),color[color_name],-1)
                a+=1
                current_state.append(color_name)

            k = cv2.waitKey(5) & 0xFF
            if k == ord('q'):
                break
            elif k ==ord('u'):
                self.state['up']=current_state
                self.check_state.append('u')
            elif k ==ord('r'):
                self.check_state.append('r')
                self.state['right']=current_state
            elif k ==ord('l'):
                self.check_state.append('l')
                self.state['left']=current_state
            elif k ==ord('d'):
                self.check_state.append('d')
                self.state['down']=current_state
            elif k ==ord('f'):
                self.check_state.append('f')
                self.state['front']=current_state
            elif k ==ord('b'):
                self.check_state.append('b')
                self.state['back']=current_state
            elif k == ord('\r'):
                # process(["R","R'"])
                if len(set(self.check_state))==6:
                    #Scan xong, lưu kết quả vào biến state
                    print("hi")
                    #lay cong thuc giai, dao nguoc va cho khoi rubik chay
                    try:
                        values = detect_solve(self.state)
                        self.solution = values
                        #self.solution = list(values.split(" "))
                        values = list(values.split(" "))
                        values.reverse()
                        print(values)
                        self.delay_move = 0
                        self.speed_up_move = 0
                        for value in values:
                            value = self.re_conv[value]
                            lis_value = list(value)
                            if lis_value[-1] == '2':
                                lis_value.pop(-1)
                                value = ''.join(lis_value)
                                self.move(value)
                                self.move(value)
                                print('moving ' + value)
                            else:
                                self.move(value)
                                print('moving ' + value)
                        self.delay_move = 0.08
                        self.my_step.text = dedent("Quét thành công, ấn I để bắn đầu giải")
                        break

                    except:
                        print("rubik error, scan again, maybe wrong something idiot!")


                else:
                    #Chưa scan xong, thiếu mặt cần scan
                    print("")
                    print("left to scan:",6-len(set(self.check_state)))

            cv2.imshow('preview',preview)
            cv2.imshow('frame',img[0:500,0:500])
        cv2.destroyAllWindows()

    def step_solve(self):
        if self.solution == "":
            print("solution is emty! Try scan your cube again")
        else:
            if self.firstCall:
                print("solution is: " + self.solution)
                self.myvalues = self.solution
                self.myvalues = list(self.myvalues.split(" "))
                self.step = 0
                self.firstCall = False
            self.speed_up_move = self.normal_move + 0.5
            self.delay_move = 0
            # lis_value = list(self.myvalues[self.step])
            # if lis_value[-1] == '2':
            #     lis_value.pop(-1)
            #     self.myvalues[self.step] = ''.join(lis_value)
            #     self.move(self.myvalues[self.step].lower())
            #     self.move(self.myvalues[self.step].lower())
            #     print('moving ' + self.myvalues[self.step])
            # else:
            self.move(self.myvalues[self.step].lower())
            print('moving ' + self.myvalues[self.step])
            self.step += 1

            if self.step == len(self.myvalues):
                self.step = 0
                self.firstCall = True
                self.delay_move = 0.08
                self.solution = ""


        # for value in values:
        #     lis_value = list(value)
        #     if lis_value[-1] == '2':
        #         lis_value.pop(-1)
        #         value = ''.join(lis_value)
        #         self.move(value)
        #         self.move(value)
        #         print('moving ' + value)
        #     else:
        #         self.move(value)
        #         print('moving ' + value)

    def move(self, value):
        if value == 'l' :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',-90)
        if value == 'd':
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',-90)
        if value == 'r':
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',90)
        if value == 'f':
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',90)
        if value == 'b':
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',-90)
        if value == 'u':
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',90)

        if value == "l'" :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',90)
        if value == "d'":
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',90)
        if value == "r'":
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',-90)
        if value == "f'":
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',-90)
        if value == "b'":
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',90)
        if value == "u'":
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',-90)

        if value == 'l2' :
            self.animation_time = self.speed_up_move
            self.rotate_side('LEFT',-180)
        if value == 'd2':
            self.animation_time = self.speed_up_move
            self.rotate_side('DOWN',-180)
        if value == 'r2':
            self.animation_time = self.speed_up_move
            self.rotate_side('RIGHT',180)
        if value == 'f2':
            self.animation_time = self.speed_up_move
            self.rotate_side('FRONT',180)
        if value == 'b2':
            self.animation_time = self.speed_up_move
            self.rotate_side('BACK',-180)
        if value == 'u2':
            self.animation_time = self.speed_up_move
            self.rotate_side('UP',180)

        self.my_step.text = dedent(value.upper())

        # self.my_step.text = dedent(value.upper()).strip()





    def input(self, key):
        if key == 'o':
            self.my_step.text = dedent("Đang mở camera,...")
            print("opening camera...")
            self.rubik_detect()

        if key == 's':
            self.scramble()

        if key == 'i':
            self.animation_time = self.normal_move
            self.step_solve()
        if key == 'l' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('LEFT',-90)
        if key == 'd' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('DOWN',-90)
        if key == 'r' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('RIGHT',90)
        if key == 'f' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('FRONT',90)
        if key == 'b' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('BACK',-90)
        if key == 'u' and self.action_trigger:
            self.animation_time = self.normal_move
            self.rotate_side('UP',90)








rubik = RubikCube()








app.run()