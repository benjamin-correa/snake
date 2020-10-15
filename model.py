import numpy as np

import transformations as tr
import easy_shaders as es
import scene_graph as sg
import basic_shapes as bs

class Snake (object):

    def __init__ (self):
        gpu_principal_quad = es.toGPUShape(
            bs.createColorQuad(246/255, 252/255, 116/255))
        head = sg.SceneGraphNode("head")
        head.transform = tr.translate(0,0,0)
        head.childs += [gpu_principal_quad]
        self.posx = 0 
        self.posy = 0
        self.direction = "UP"
        self.model = head
        self.on = True
        
    def draw (self, pipeline, N):
        self.model.transform = tr.matmul([
            tr.translate(self.posx,self.posy,0), tr.uniformScale(1/N)])
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def update(self, N):
        if self.direction == "UP":
            self.posy += 1/N
        elif self.direction == "DOWN":
            self.posy -= 1/N
        elif self.direction == "LEFT":
            self.posx -= 1/N
        elif self.direction == "RIGHT":
            self.posx += 1/N

    def borderCollision (self, N):
        if self.posx >= 1 - (1/(2*N)) or self.posy >= 1 - (1/(2*N)):
            self.on = False
            print("Game Over")
        elif self.posx <= -1 + (1/(2*N)) or self.posy <= -1 + (1/(2*N)):
            self.on = False
            print("Game Over")

    def appleEaten (self, N, apple):
        if ((apple.posx - 1/N < self.posx < apple.posx +1/N) and 
            (apple.posy - 1/N < self.posy < apple.posy +1/N)):
            x = np.random.randint(-10 , 10)
            y = np.random.randint(-10 , 10)

            if x < 0 and y < 0:
                apple.posx = x/10 + (1/(N))
                apple.posy = y/10 + (1/(N))
            elif x >= 0 and y < 0:
                apple.posx = x/10 - (1/(N))
                apple.posy = y/10 + (1/(N))
            elif x >= 0 and y >= 0:
                apple.posx = x/10 - (1/(N))
                apple.posy = y/10 - (1/(N))
            elif x < 0 and y >= 0:
                apple.posx = x/10 + (1/(N))
                apple.posy = y/10 - (1/(N))

            print("Comiste ñam")




class Scene (object):
    def __init__ (self):
        gpu_head_quad = es.toGPUShape(
            bs.createColorQuad(40/255, 186/255, 35/255))
        border = sg.SceneGraphNode("border")
        border.transform = tr.translate(0,0,0)
        border.childs += [gpu_head_quad]
        transform_border = sg.SceneGraphNode('borderTR')
        transform_border.childs += [border]

        self.model = transform_border
        self.posx = 0
        self.posy = 0

    def draw (self, pipeline, N):
        self.model.transform = tr.scale(2 - (1 / N), 2 - (1 / N), 1)
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')





class Apple (object):

    def __init__ (self):
        gpu_apple_quad = es.toGPUShape(
            bs.createColorDegradeQuad(217/255, 22/255, 22/255,
             217/255, 100/255, 150/255))
        apple = sg.SceneGraphNode("apple")
        apple.transform = tr.translate(0,0,0)
        apple.childs += [gpu_apple_quad]

        gpu_stick_quad = es.toGPUShape(
            bs.createColorQuad(69/255, 29/255, 4/255))
        stick = sg.SceneGraphNode("stick")
        stick.transform = tr.matmul([
            tr.translate(0,0.6,0), tr.scale(0.15, 0.30, 1)])
        stick.childs += [gpu_stick_quad]

        gpu_leaf_quad = es.toGPUShape(
            bs.createColorQuad(38/255, 128/255, 33/255))
        leaf = sg.SceneGraphNode("leaf")
        leaf.transform = tr.matmul([
            tr.translate(0.20,0.6,0),
             tr.scale(0.25, 0.15, 1), tr.rotationZ(0.5)])
        leaf.childs += [gpu_leaf_quad]

        apple_stick_leaf = sg.SceneGraphNode("apple_stick_leaf")
        apple_stick_leaf.childs += [apple, stick, leaf]
        transform_apple = sg.SceneGraphNode('appleTR')
        transform_apple.childs += [apple_stick_leaf]

        self.model = transform_apple
        self.posx = 0
        self.posy = 0

    def draw (self, pipeline, N):
        self.model.transform = tr.matmul([
            tr.translate(self.posx,self.posy,0), tr.uniformScale(1/N)])
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

