import os

os.environ['QT_API'] = 'pyqt5'
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpinBox, QApplication, QPushButton, QColorDialog, QFileDialog


# first thing's first, create the QApplication
app = QApplication([])

# setup our widgets.  These are things that hold values and also know how to display themselves in a gui
spinBox = QSpinBox()
spinBox.setValue(7)
button = QPushButton('Bump Value')
button2 = QPushButton('Pick Color')
button3 = QPushButton('Browse')

# connect callback functions to the buttons
def bumpValue():
    spinBox.setValue(spinBox.value() + 1)

def pickColor():
    dialog = QColorDialog()
    dialog.exec_()
    color = dialog.currentColor()
    print(f'Picked {color}') 

def browseFile():
    dialog = QFileDialog()
    dialog.exec_()
    files = dialog.selectedFiles()
    print(f'Picked {files}')


button.clicked.connect(bumpValue)   # 'button.clicked' is a 'signal' which is emitted when button is clicked
button2.clicked.connect(pickColor)
button3.clicked.connect(browseFile)

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


