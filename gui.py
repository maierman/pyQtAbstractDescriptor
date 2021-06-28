from qtpy.QtGui import QColor, QPen
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy
from pyqtgraph import GraphicsLayoutWidget, ScatterPlotItem
import numpy as np
from functools import partial
from widgets import ControlWidget, StarWidget


class StarItem(QGraphicsEllipseItem):
    def __init__(self, starModel):
        self.starModel = starModel
        size = 10
        super().__init__(-size/2, -size/2, size, size)
        self.setPen(QColor(148, 32, 25))
        self.setBrush(QColor(148, 32, 25))
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setFlag(QGraphicsItem.ItemIgnoresTransformations)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            # when our position changes update the model
            self.starModel.x = int(value.x())
            self.starModel.y = int(value.y())
        return super().itemChange(change, value)


class MainGui(QWidget):
    @staticmethod
    def rainbowColor(a):
        """Returns a color on the 'rainbow' spectrum where a is expected to be between 0 and 1"""
        x = a * 5
        red = 255 if x < 2 else ( 255 * ( 3 - x ) if x < 3 else (0 if x < 4 else 120 * (5 - x)))
        green = 120 * x if x < 2 else (240 if x < 3 else (240 * ( 4 - x ) if x < 4 else 0))
        blue = 0 if x < 2 else ( 30 * ( 3 - x) if x < 3 else (30 + 225 * ( 4 - x) if x < 4 else 255))
        return red, green, blue

    def __init__(self, engine, controlModel):
        super().__init__()
        self.engine = engine
        self.controlModel = controlModel
        self.rainbowPen = None
        self.rainbowBrush = None
        self.starMap = {}  # an internal map from starModels to (guiWidget, item)

        # setup subscriptions for adding stars
        self.engine.sigNewStar.connect(self.addStar)
        self.engine.sigDeleteStar.connect(self.deleteStar)
        self.engine.sigResetPlanets.connect(self.buildColorPalette)

        graph = GraphicsLayoutWidget()
        self.view = graph.addViewBox()   # this is the pyqtgraph view element that lets us zoom and pan

        # setup the scatterplot that will show the planets
        self.plot = ScatterPlotItem()
        self.view.addItem(self.plot)
        self.view.setAspectLocked(True)
        self.view.setRange(xRange=(-100, 100), yRange=(-100, 100))

        # create widgets for controls and stars
        self.controlLayout = QVBoxLayout()
        self.controlLayout.addWidget(ControlWidget(controlModel, engine), 0)
        self.starLayout = QVBoxLayout()
        self.starLayout.addStretch(0) # we'll keep this stretch at the end so widgets float to top of layout
        self.engine.addStar()
        self.starListWidget = QWidget()
        self.starListWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.starListWidget.setLayout(self.starLayout)
        self.starScrollArea = QScrollArea()
        self.starScrollArea.setWidget(self.starListWidget)
        self.starScrollArea.setWidgetResizable(True)
        self.starScrollArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        self.starScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.controlLayout.addWidget(self.starScrollArea)

        # and now the main layout
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(graph, 1)
        mainLayout.addLayout(self.controlLayout)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        self.setLayout(mainLayout)

    def buildColorPalette(self, N):
        colors = [self.rainbowColor(i/N) for i in range(N)]
        self.rainbowBrush = [QColor(*c) for c in colors]
        self.rainbowPen = [QPen(b) for b in self.rainbowBrush]

    def addStar(self, star):
        starWidget = StarWidget(star)          # this is the gui controls for the star
        starWidget.delete.clicked.connect(partial(self.engine.deleteStar, star))
        starItem = StarItem(star)              # this is the QGraphicsItem for displaying the star
        self.starMap[star] = (starWidget, starItem)
        self.starLayout.insertWidget(self.starLayout.count()-1, starWidget)
        self.view.addItem(starItem)

    def deleteStar(self, star):
        starWidget, starItem = self.starMap[star]
        starWidget.hide()
        starWidget.deleteLater()
        starItem.hide()
        del starItem
        del self.starMap[star]

    def updatePlanets(self):
        if len(self.engine.px):
            color = (90, 120, 150)   # a nice pale bluish color
            x = self.engine.px
            y = self.engine.py
            if self.controlModel.rainbow:
                v = np.sqrt(np.power(x, 2) + np.power(y, 2))
                s = np.argsort(v)
                self.plot.setData(x=x[s], y=y[s], symbol='o', pen=self.rainbowPen, brush=self.rainbowBrush, size=1)
            else:
                self.plot.setData(x=x, y=y, symbol='o', pen=color, brush=color, size=2)
