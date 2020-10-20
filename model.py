import numpy as np

import transformations as tr
import easy_shaders as es
import scene_graph as sg
import basic_shapes as bs
from OpenGL.GL import *

class Snake (object):
    """
    Creates the snake's head, and implements
    the head movement logic.
    """

    def __init__ (self):
        gpu_head_quad = es.toGPUShape(
            bs.createTextureQuad("img/Snake_Head.png"), GL_REPEAT, GL_NEAREST)
        head = sg.SceneGraphNode("head")
        head.transform = tr.translate(0,0,0)
        head.childs += [gpu_head_quad]
        self.posx = 0 
        self.posy = 0
        self.direction = "UP"
        self.model = head
        self.on = True
        
    def draw (self, pipeline, N):
        self.model.transform = np.matmul(
            tr.translate(self.posx,self.posy,0), tr.uniformScale(1/N))
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

class Body(object):
    """
    Draws and implements the body of the snake.
    """
    def __init__ (self, x, y):
        gpu_body_quad = es.toGPUShape(
            bs.createTextureQuad("img/Snake_Body.png"), GL_REPEAT, GL_NEAREST)
        body = sg.SceneGraphNode("body")
        body.transform = tr.translate(0,0,0)
        body.childs += [gpu_body_quad]
        self.posx = x
        self.posy = y
        self.model = body
    
    def draw(self, pipeline, N):
        self.model.transform = tr.matmul([
            tr.translate(self.posx, self.posy, 0),
            tr.uniformScale( 1/N )])
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')


class Logic(object):
    """
    This holds the main logic of the game, the movement
    of the body logic, the adding of a body logic, the collisions logics
    and the apple logics
    """
    def __init__ (self, snake):
        self.head = snake
        self.body = []

    def addBody (self):
        """
        Appends a body part on the end
        """
        if len(self.body) == 0:
            self.body.append(Body(self.head.posx, self.head.posy))
        else:
            self.body.append(Body(self.body[len(self.body)-1].posx, self.body[len(self.body)-1].posy))

    def movement (self, N):
        """
        Movement of the body
        """
        x_head = self.head.posx
        y_head = self.head.posy
        self.head.update(N)

        for i in range(len(self.body)):
            x_copy = self.body[i].posx
            y_copy = self.body[i].posy
            self.body[i].posx = x_head
            self.body[i].posy = y_head
            x_head = x_copy
            y_head = y_copy
        
    def bodyCollision(self, N):
        """
        Checks if the snake is colliding with his body
        """
        x_head = self.head.posx
        y_head = self.head.posy
        for i in self.body:
            if ((i.posx - 1/(2*N) < x_head < i.posx +1/(2*N)) and
                (i.posy - 1/(2*N) < y_head < i.posy +1/(2*N))):
                self.head.on = False
                print("Game Over, tu puntaje es:", len(self.body))
    
    def borderCollision (self, N):
        """
        Checks if the snake is colliding with the border
        """

        x_head = self.head.posx
        y_head = self.head.posy
        if x_head >= 1 - (1/(2*N)) or y_head >= 1 - (1/(2*N)):
            self.head.on = False
            print("Game Over, tu puntaje es:", len(self.body))
        elif x_head <= -1 + (1/(2*N)) or y_head <= -1 + (1/(2*N)):
            self.head.on = False
            print("Game Over, tu puntaje es:", len(self.body))

    def appleEaten (self, N, apple):
        """
        First we check if the apple is goin to be eaten by the snake,
        then we a start a cycle where generates 2 random numbers and
        those numbers will be the candidate coordinates, the we check
        if the apple is goin to be in a empty space, if is not going on
        a empty space, we generate 2 new numbers.
        """
        x_head = self.head.posx
        y_head = self.head.posy
        if ((apple.posx - 1/(2*N) < x_head < apple.posx +1/(2*N)) and 
            (apple.posy - 1/(2*N) < y_head < apple.posy +1/(2*N))):

            self.addBody()

            

            while True:

                aux = 0 #Helps to see if the apple is goin to go on a empty space
                x = np.random.randint(-10 , 10)
                y = np.random.randint(-10 , 10)
                for i in self.body:
                    if x < 0 and y < 0:
                        apple.posx = x/10 + (1/(N))
                        apple.posy = y/10 + (1/(N))
                        if not ((apple.posx - 1/N < i.posx < apple.posx +1/N) and 
                            (apple.posy - 1/N < i.posy < apple.posy +1/N)): 
                            aux += 1
                        else:
                            break

                    elif x >= 0 and y < 0:
                        apple.posx = x/10 - (1/(N))
                        apple.posy = y/10 + (1/(N))
                        if not ((apple.posx - 1/N < i.posx < apple.posx +1/N) and 
                            (apple.posy - 1/N < i.posy < apple.posy +1/N)): 
                            aux += 1
                        else:
                            break
                    elif x >= 0 and y >= 0:
                        apple.posx = x/10 - (1/(N))
                        apple.posy = y/10 - (1/(N))
                        if not ((apple.posx - 1/N < i.posx < apple.posx +1/N) and 
                            (apple.posy - 1/N < i.posy < apple.posy +1/N)): 
                            aux += 1
                        else:
                            break
                    elif x < 0 and y >= 0:
                        apple.posx = x/10 + (1/(N))
                        apple.posy = y/10 - (1/(N))
                        if not ((apple.posx - 1/N < i.posx < apple.posx +1/N) and 
                            (apple.posy - 1/N < i.posy < apple.posy +1/N)): 
                            aux += 1
                        else:
                            break
                if aux == len(self.body):
                    break
                
            #print("Comiste ñam")

    def draw(self, pipeline, N):
        for x in self.body:
            x.draw(pipeline, N)


class Scene (object):
    """
    Creates the borders of the map
    """
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
    """
    Creates the apple shape
    """
    def __init__ (self,N):
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
        self.posy = 1/N

    def draw (self, pipeline, N):
        self.model.transform = tr.matmul([
            tr.translate(self.posx,self.posy,0), tr.uniformScale(1/N)])
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

class EndScreeen(object):

    """
    Displays the game over texture
    """

    def __init__(self):
        gpu_end_quad = es.toGPUShape(
                bs.createTextureQuad("img/GO.png"), GL_REPEAT, GL_NEAREST)
        end = sg.SceneGraphNode("end")
        end.transform = tr.translate(0,0,0)
        end.childs += [gpu_end_quad]
        self.posx = 0 
        self.posy = 0
        self.model = end
        
    def draw (self, pipeline, N):
        self.model.transform = np.matmul(
            tr.translate(self.posx+0.1,self.posy+0.05, 0), tr.rotationZ(np.pi/6))
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')