import cx_Freeze
from cx_Freeze import *
import sys


sys.argv.append("build")





setup(
    name = "MyRubik",
    version = '0.1',
    description = "This is description",
    options = {"build_exe": {"packages": ['ursina']}},
    executables = [
        Executable(
            target_name= "My Rubik Cube",
            script="main.py",
            icon="assets/textures/my_dog_icon.ico",
            base = "Win32GUI"
        )
    ]
)