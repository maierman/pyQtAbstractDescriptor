"""This is a fun toy example which shows how you can use the AbstractDescriptorModel to simplify usage
of the Qt model view architecture
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
os.environ['QT_API'] = 'pyqt5'
os.environ['PYQTGRAPH_QT_LIB'] = 'PyQt5'

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import QTimer, Signal, QObject
import qdarkstyle
import numpy as np
from models import StarModel, ControlModel
from gui import MainGui


class Engine(QObject):
    sigNewStar = Signal(object)      # signals that a new star is born
    sigDeleteStar = Signal(object)   # signals that a star has gone away
    sigResetPlanets = Signal(object)  # object = numPlanets.

    def __init__(self, controlModel):
        super().__init__()
        self.controlModel = controlModel

        # planet positions
        self.px = np.array([])
        self.py = np.array([])
        self.vx = np.array([])
        self.vy = np.array([])

        self.stars = []

    def addStar(self):
        star = StarModel(0, 0)
        self.stars.append(star)
        self.sigNewStar.emit(star)

    def deleteStar(self, star):
        self.stars.remove(star)
        self.sigDeleteStar.emit(star)

    def resetPlanets(self, x, y, std=50):
        """get rid of current planets and draw a new set with a gaussian distribution centered about x, y
        with zero velocity
        """
        N = int(self.controlModel.numPlanets)

        self.px = np.random.normal(x, 50, N)
        self.py = np.random.normal(y, 50, N)
        self.vx = np.full(N, 0.0)
        self.vy = np.full(N, 0.0)
        self.sigResetPlanets.emit(N)

    def reverseTime(self):
        self.vx *= -1
        self.vy *= -1

    def step(self, dt):
        """Elapse time by dt and update all positions and velocities
        """
        if len(self.px):
            self.px += self.vx * dt
            self.py += self.vy * dt

            for star in self.stars:
                r = np.sqrt(np.power(self.px - star.x, 2) + np.power(self.py - star.y, 2))
                r_hooke = np.power(r, self.controlModel.k_pow - 1)
                k = self.controlModel.k

                ax = (star.x - self.px) * r_hooke * k
                ay = (star.y - self.py) * r_hooke * k

                self.vx += ax * dt
                self.vy += ay * dt


if __name__ == '__main__':

    app = QApplication([])
    app.setStyle('Fusion')
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api=os.environ['QT_API']))

    controlModel = ControlModel()
    engine = Engine(controlModel)
    gui = MainGui(engine, controlModel)
    gui.show()

    def step():
        engine.step(0.005)       # time step of 0.005 seems good for current params
        gui.updatePlanets()

    timer = QTimer()
    timer.timeout.connect(step)
    timer.start(16)

    QApplication.instance().exec_()
