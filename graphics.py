from OpenGL.GL import *
from PyQt5.QtOpenGL import QGLWidget
import numpy as np
from numpy.linalg import norm, inv
import glm

class GraphicsManager(QGLWidget):
    def __init__(self, engine):
        QGLWidget.__init__(self)
        self.engine = engine

        self.pos = np.array([0.0, 50.0, 200.0], np.float32)
        self.direction = np.array([0.0,-50.0,-200.0], np.float32)
        self.up = np.array([0.0, 1.0, 0.0], np.float32)

        self.cameraRotateX = self.cameraRotateY = 0.0

        self.programs = {}
        self.shaders = {}


    def initializeGL(self):
        glClearColor(0,1,0,1)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

        #glEnable(GL_TEXTURE_2D)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


        self.updateView()
        self.projection = glm.perspective(45.0, float(self.width()) / float(self.height()), 0.01, 1000.0)
        glViewport(0,0, self.width(), self.height())

        shader_data = [self.loadShader('shaders/colorvert.vs', GL_VERTEX_SHADER), self.loadShader('shaders/colorfrag.fs', GL_FRAGMENT_SHADER)]
        self.createShaderProgram('color', shader_data)

        shader_data = [self.loadShader('shaders/grayvert.vs', GL_VERTEX_SHADER), self.loadShader('shaders/grayfrag.fs', GL_FRAGMENT_SHADER)]
        self.createShaderProgram('gray', shader_data)

        shader_data = [self.loadShader('shaders/fontvert.vs', GL_VERTEX_SHADER), self.loadShader('shaders/fontfrag.fs', GL_FRAGMENT_SHADER)]
        self.createShaderProgram('gui', shader_data)


    def paintGL(self):
        self.updateCamera()
        self.updateView()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.programs['color'])
        #for ent in self.engine.entityManager.entities:
        #    ent.render()

        glUseProgram(0)

    def createProjection(self, fovy, aspect, near, far):
        projection = np.array([
                                [fovy/aspect, 0, 0, 0],
                                [0, fovy, 0, 0],
                                [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
                                [0, 0, -1, 0]
                             ], np.float32)

        return projection

    def updateView(self):
        temp = self.pos - (self.pos + self.direction)
        Z = temp / norm(temp)
        temp = np.cross(self.up, Z)
        X = temp / norm(temp)

        Y = np.cross(Z,X)

        mat = np.array([
                        [X[0], X[1], X[2], 0],
                        [Y[0], Y[1], Y[2], 0],
                        [Z[0], Z[1], Z[2], 0],
                        [self.pos[0], self.pos[1], self.pos[2], 1]
                        ], np.float32)

        self.view = inv(mat)

    def loadShader(self, shaderFile, shaderType):
        with open(shaderFile) as fin:
            shaderStr = fin.read()

            shader = glCreateShader(shaderType)
            glShaderSource(shader, shaderStr)
            glCompileShader(shader)

            log = glGetShaderInfoLog(shader)
            status = glGetShaderiv(shader, GL_COMPILE_STATUS, None)
            if not status:
                print("Error:", log)

            return shader

    def createShaderProgram(self, name, shader_vec):
        program = glCreateProgram()
        for shader in shader_vec:
            glAttachShader(program, shader)

        glLinkProgram(program)

        status = glGetProgramiv(program, GL_LINK_STATUS)
        if not status:
            print("Unable to create shader program!")
            self.engine.stop()

        self.programs[name] = program
        self.shaders[name] = shader_vec

        return program

    def updateCamera(self):
        pass