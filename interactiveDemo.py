"""This is an example script showing how to use the combination of AbstractDescriptorModel
and DescriptorModelItem
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))


os.environ['QT_API'] = 'pyqt5'
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontDatabase, QFont
from qtpy.QtWidgets import QWidget, QSpinBox, QLabel, QVBoxLayout, QGridLayout, QApplication, QPushButton, QCheckBox, QTextEdit, QFrame,\
    QRadioButton, QComboBox, QLineEdit, QSlider, QDial, QHBoxLayout
from AbstractDescriptorModel import AbstractDescriptorModel, DescriptorModelItem
from ExtDataWidgetMapper import ExtDataWidgetMapper
from ConsoleWidget import ConsoleWidget
from ColorButtonWidget import ColorButton
from LogSliderWidget import LogSliderWidget


class OurDataModel(AbstractDescriptorModel):
    # these are descriptors that we need to setup as class attributes.
    spinBox = DescriptorModelItem(7)
    checkBox = DescriptorModelItem(False)
    comboBox = DescriptorModelItem('a')
    slider = DescriptorModelItem(1)
    logSlider = DescriptorModelItem(1)   
    dial = DescriptorModelItem(1)
    radioButton = DescriptorModelItem(True)
    lineEdit = DescriptorModelItem()

    # these initializations are optional but usually desired.  Without them the attributes will still exist
    # but will be initialized to None unless initialized above at the class level
    def __init__(self):
        super().__init__()
        self.lineEdit = 'text!!' 


# first thing's first, create the QApplication
app = QApplication([])

# here's our data
model = OurDataModel()

# here's widgets that we'll use to control the data
# we'll put them all into a layout
widgetLayout = QGridLayout()
widgetLayout.setColumnMinimumWidth(0, 100)
widgetLayout.setColumnMinimumWidth(1, 100)

sb = QSpinBox()
widgetLayout.addWidget(QLabel('spinBox'), 0, 0)
widgetLayout.addWidget(sb, 0, 1)

b = QCheckBox()
widgetLayout.addWidget(QLabel('checkBox'), 1, 0)
widgetLayout.addWidget(b, 1, 1)

rb = QRadioButton()
widgetLayout.addWidget(QLabel('radioButton'), 2, 0)
widgetLayout.addWidget(rb, 2, 1)

le = QLineEdit()
widgetLayout.addWidget(QLabel('lineEdit'), 3, 0)
widgetLayout.addWidget(le, 3, 1)

s = QSlider(Qt.Horizontal)
widgetLayout.addWidget(QLabel('slider'), 4, 0)
widgetLayout.addWidget(s, 4, 1)

ls = LogSliderWidget(Qt.Horizontal)
widgetLayout.addWidget(QLabel('logSlider'), 5, 0)
widgetLayout.addWidget(ls, 5, 1)

d = QDial()
d.setWrapping(True)
widgetLayout.addWidget(QLabel('dial'), 6, 0)
widgetLayout.addWidget(d, 6, 1)

cb = QComboBox()
cb.insertItems(0, ['a', 'b', 'c', 'd'])
widgetLayout.addWidget(QLabel('comboBox'), 7, 0)
widgetLayout.addWidget(cb, 7, 1)

textArea = QTextEdit()
message = """This demo shows how to use the AbstractDescriptorModel class to connect gui elements to object attributes.  

For example, entering 'model.numericVal = 1234' in the IPython console and you'll see the value update in the gui.  

Similarly, any value set in the gui can be read directly from the attribute"""
textArea.setText(message)

# now here's the magic.  Map widgets to model using mapper.  All of these lines are super important
# don't forget any of them.  Especially not mapper.toFirst()
mapper = ExtDataWidgetMapper()
mapper.setOrientation(Qt.Vertical)  # AbstractDescriptorModel internally uses a 'vertical' arrangement
mapper.setModel(model)

mapper.addMapping(sb, OurDataModel.spinBox.section)
mapper.addMapping(b, OurDataModel.checkBox.section)
mapper.addMapping(rb, OurDataModel.radioButton.section)
mapper.addMapping(le, OurDataModel.lineEdit.section)
mapper.addMapping(s, OurDataModel.slider.section)
mapper.addMapping(ls, OurDataModel.logSlider.section)
mapper.addMapping(d, OurDataModel.dial.section, b'value')
mapper.addMapping(cb, OurDataModel.comboBox.section, b'currentText')
mapper.toFirst()    # call this AFTER setting up the mappings in order to sync data from the model to the gui

# NOTE:  note that the gui will not show the same value as the model when the model values are out of range for
# the gui widgets.  This can happen when ranges are exceeded or when a value is not allowed for a QComboBox, etc...

# create a console so that we can show that programatically changing a variable
# changes the GUI.  Push
console = ConsoleWidget()
console.push_vars({'model': model})

lowerLayout = QHBoxLayout()
lowerLayout.addLayout(widgetLayout)
lowerLayout.addWidget(console)

mainLayout = QVBoxLayout()
mainLayout.addWidget(textArea)
mainLayout.addLayout(lowerLayout)

# create our main window
win = QWidget()
win.setLayout(mainLayout)
win.move(200, 100)
win.resize(800, 500)
win.show()
win.raise_()

# and finally start the Qt event loop
QApplication.instance().exec_()


