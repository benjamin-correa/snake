import glfw
from OpenGL.GL import *
import sys
from model import *
from controller import Controller

N = int(sys.argv[1])

speed = 2/N

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

    glClearColor(16/255, 74/255, 3/255, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    snake = Snake()

    controller.set_model(snake)

    apple = Apple(N)

    border = Scene()

    logic = Logic(snake)

    end = EndScreeen()

    t0 = 0

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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
        apple.draw(pipeline, N)
        glUseProgram(pipeline2.shaderProgram)
        snake.draw(pipeline2, N)
        logic.draw(pipeline2, N)

        if dt >= speed and snake.on:
            logic.movement(N)
            logic.borderCollision(N)
            logic.bodyCollision(N)
            logic.appleEaten(N, apple)
            t0 = ti

        if snake.on == False:
            end.draw(pipeline2, N)
        

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)
        

    glfw.terminate()