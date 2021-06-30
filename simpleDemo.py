import os

os.environ['QT_API'] = 'pyqt5'
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QApplication, QPushButton


# first thing's first, create the QApplication
app = QApplication([])

# setup our widgets.  These are things that hold values and also know how to display themselves in a gui
spinBox = QSpinBox()
spinBox.setValue(7)
button = QPushButton('Bump Value')
button2 = QPushButton('Do Nothing')
button3 = QPushButton('Do Nothing')

# connect a function to the button
def bumpValue():
    spinBox.setValue(spinBox.value() + 1)
button.clicked.connect(bumpValue)   # 'button.clicked' is a 'signal' which is emitted when button is clicked

# put the buttons together in a horizontal layout
buttonLayout = QHBoxLayout()
buttonLayout.addWidget(button)
buttonLayout.addWidget(button2)
buttonLayout.addWidget(button3)

# layouts hold widgets and can also hold other layouts
mainLayout = QVBoxLayout()
mainLayout.addLayout(buttonLayout)
mainLayout.addWidget(spinBox)

# create our main window
win = QWidget()
win.setLayout(mainLayout)
win.move(200, 100)
win.resize(200, 100)
win.show()
win.raise_()

# and finally start the Qt event loop
QApplication.instance().exec_()


