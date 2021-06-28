from qtpy.QtWidgets import QPushButton, QLCDNumber, QWidget, QGridLayout, QVBoxLayout, QFrame, QLabel, QSizePolicy
from qtpy.QtCore import Qt
from functools import partial
from LCDNumberView import LCDNumberView
from LogSliderWidget import LogSliderWidget
from ExtDataWidgetMapper import ExtDataWidgetMapper


# a gui for a star
class StarWidget(QFrame):
    def __init__(self, starModel):
        super().__init__()
        self.delete = QPushButton('DELETE')
        self.delete.setStyleSheet('color: #942019;')

        self.x = QLCDNumber()
        self.y = QLCDNumber()

        self.mapper = ExtDataWidgetMapper()
        self.mapper.setOrientation(Qt.Vertical)

        self.setupUI()
        self.mapWidgets(starModel)

    # noinspection PyArgumentList
    def setupUI(self):
        layout = QGridLayout()

        layout.addWidget(QLabel('STAR COORD'), 0, 0, 1, 2)
        layout.addWidget(self.x, 0, 2)
        layout.addWidget(self.y, 0, 3)

        layout.addWidget(self.delete, 0, 5)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setLayout(layout)

    def mapWidgets(self, starModel):
        # first deal with the model mapping
        self.mapper.setModel(starModel)
        self.mapper.addMapping(self.x, type(starModel).x.section, b'value')   # QLCDLabel requires use of 'value' here
        self.mapper.addMapping(self.y, type(starModel).y.section, b'value')
        self.mapper.toFirst()


# and a gui widget for the main controls.  They are linked to the controlModel and the engine
class ControlWidget(QWidget):
    def __init__(self, controlModel, engine):
        super().__init__()
        self.controlModel = controlModel
        self.k = LogSliderWidget(Qt.Horizontal)
        self.k.setRange(1E-8, 100)
        self.k_display = LCDNumberView(integerDisplay=False)

        self.k_pow = LogSliderWidget(Qt.Horizontal)
        self.k_pow.setRange(1, 3)
        self.k_pow_display = LCDNumberView(integerDisplay=False)
        self.k_pow_display.setNumDigits(4)

        self.N = LogSliderWidget(Qt.Horizontal)
        self.N.setRange(1, 10000)
        self.N_display = LCDNumberView()

        self.addStar = QPushButton('ADD STAR')
        self.reverseTime = QPushButton('REVERSE TIME')
        self.rainbow = QPushButton('RAINBOW')
        self.resetPlanets = QPushButton('RESET PLANETS')

        self.mapper = ExtDataWidgetMapper()
        self.mapper.setOrientation(Qt.Vertical)

        self.setupUI()
        self.mapWidgets(controlModel, engine)

    def setupUI(self):
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        layout = QGridLayout()
        layout.addWidget(QLabel('HOOKE CONSTANT'), 0, 0)
        layout.addWidget(self.k, 0, 1, 1, 3)
        layout.addWidget(self.k_display, 0, 4)

        layout.addWidget(QLabel('HOOKE POWER'), 1, 0)
        layout.addWidget(self.k_pow, 1, 1, 1, 3)
        layout.addWidget(self.k_pow_display, 1, 4)

        layout.addWidget(QLabel('NUM PLANETS'), 2, 0)
        layout.addWidget(self.N, 2, 1, 1, 3)
        layout.addWidget(self.N_display, 2, 4)

        buttonLayout = QGridLayout()
        buttonLayout.addWidget(self.addStar, 0, 0)
        buttonLayout.addWidget(self.reverseTime, 0, 1)
        buttonLayout.addWidget(self.rainbow, 1, 0)
        buttonLayout.addWidget(self.resetPlanets, 1, 1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def mapWidgets(self, controlModel, engine):
        self.mapper.setModel(controlModel)
        self.mapper.addMapping(self.k, type(controlModel).k.section)
        self.mapper.addMapping(self.k_pow, type(controlModel).k_pow.section)
        self.mapper.addMapping(self.N, type(controlModel).numPlanets.section)
        self.mapper.toFirst()

        self.k_display.setModel(controlModel, type(controlModel).k.section)
        self.k_pow_display.setModel(controlModel, type(controlModel).k_pow.section)
        self.N_display.setModel(controlModel, type(controlModel).numPlanets.section)

        self.addStar.clicked.connect(engine.addStar)
        self.reverseTime.clicked.connect(engine.reverseTime)
        self.resetPlanets.clicked.connect(partial(engine.resetPlanets, 0, 0))
        self.rainbow.clicked.connect(self.toggleRainbow)

    def toggleRainbow(self):
        self.controlModel.rainbow = not self.controlModel.rainbow
