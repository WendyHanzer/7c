import sys
import PyQt5.QtCore as qt_core
import PyQt5.QtWidgets as qt
from PyQt5.QtOpenGL import QGLFormat
from OpenGL.GL import glGetString, GL_VERSION

from graphics import GraphicsManager

class MainWindow(qt.QMainWindow):
    def __init__(self, engine):
        qt.QMainWindow.__init__(self)
        self.engine = engine

    def keyPressEvent(self, event):
        if event.key() == qt_core.Qt.Key_Escape:
            self.engine.stop()

        else:
            print("Pressed:", event.text())

class Engine(object):
    def __init__(self):
        self.app = qt.QApplication(sys.argv)
        self.initWindow()

    def run(self):
        self.window.show()

        self.app.exec_()

    def initWindow(self):
        self.window = MainWindow(self)
        self.window.setWindowTitle('CS791a')

        glFormat = QGLFormat()
        glFormat.setDoubleBuffer(True)
        glFormat.setDirectRendering(True)
        glFormat.setProfile(QGLFormat.CoreProfile)
        glFormat.setVersion(3,3)
        QGLFormat.setDefaultFormat(glFormat)

        #glFormat.setOption(QGLFormat.OpenGL_Version_3_3)

        self.graphics = GraphicsManager(self)
        self.graphics.makeCurrent()
        self.window.setCentralWidget(self.graphics)
        self.window.resize(1600,900)

        print(glGetString(GL_VERSION))

    def stop(self):
        self.app.quit()