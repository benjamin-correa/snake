from model import *
import glfw
import sys


SIZE_IN_BYTES = 4


# A class to control the application
class Controller(object):
    def __init__(self):
        self.model = None
        

    def set_model(self, m):
        self.model = m

# we will use the global controller as communication with the callback function
    def on_key(self,window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                sys.exit()
            elif (key == glfw.KEY_UP or key == glfw.KEY_W) and self.model.direction != "DOWN":
                self.model.direction = "UP"
            elif (key == glfw.KEY_DOWN or key == glfw.KEY_S) and self.model.direction != "UP":
                self.model.direction = "DOWN"
            elif (key == glfw.KEY_LEFT or key == glfw.KEY_A) and self.model.direction != "RIGHT":
                self.model.direction = "LEFT"
            elif (key == glfw.KEY_RIGHT or key == glfw.KEY_D) and self.model.direction != "LEFT":
                self.model.direction = "RIGHT"


                






