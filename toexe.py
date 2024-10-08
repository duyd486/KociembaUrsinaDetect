import cx_Freeze
from cx_Freeze import *
import sys


sys.argv.append("build")





setup(
    name = "MY RUBIK CUBE",
    version = '1.0.0',
    description = "This is description",
    options = {"build_exe": {"packages": ['ursina']}},
    executables = [
        Executable(
            target_name= "MY RUBIK CUBE",
            script="main.py",
            icon="assets/textures/favicon.ico",
            base = "Win32GUI"
        )
    ]
)