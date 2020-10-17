import glfw
from OpenGL.GL import *
import sys
from model import *
from controller import Controller

if __name__ == '__main__':

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1000
    height = 1000

    window = glfw.create_window(width, height, 'Snake', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Assembling the shader program (pipeline) with both shaders
    pipeline = es.SimpleTransformShaderProgram()

    # Assembling the shader program (pipeline2) with both shaders
    pipeline2 = es.SimpleTextureTransformShaderProgram()
    glUseProgram(pipeline2.shaderProgram)

    glClearColor(16/255, 74/255, 3/255, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    N = 10

    snake = Snake()

    controller.set_model(snake)

    apple = Apple(N)

    border = Scene()

    logic = Logic(snake)

    t0 = 0

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input
        
        ti = glfw.get_time()
        dt = ti - t0
        
        # Using GLFW to check for input events
        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)
        # DIBUJAR LOS MODELOS
        glUseProgram(pipeline.shaderProgram)
        
        border.draw(pipeline, N)
        snake.draw(pipeline, N)
        apple.draw(pipeline, N)
        logic.draw(pipeline, N)

        if dt >= 0.2 and snake.on:
            logic.movement(N)
            logic.borderCollision(N)
            logic.bodyCollision(N)
            logic.appleEaten(N, apple)
            t0 = ti
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        

    glfw.terminate()