"""This is an example script showing how to use the combination of AbstractDescriptorModel
and DescriptorModelItem
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))


os.environ['QT_API'] = 'pyqt5'
from qtpy.QtCore import Qt
from qtpy.QtGui import QFontDatabase, QFont
from qtpy.QtWidgets import QWidget, QGroupBox, QSpinBox, QLabel, QVBoxLayout, QApplication, QPushButton, QCheckBox, QTextEdit, QFrame,\
    QRadioButton, QComboBox, QLineEdit, QSlider, QDial, QLCDNumber, QFontDialog, QHBoxLayout
from AbstractDescriptorModel import AbstractDescriptorModel, DescriptorModelItem
from ExtDataWidgetMapper import ExtDataWidgetMapper
from ConsoleWidget import ConsoleWidget
from ColorButtonWidget import ColorButton
from LogSliderWidget import LogSliderWidget


class OurDataModel(AbstractDescriptorModel):
    # these are descriptors that we need to setup as class attributes.
    numericVal = DescriptorModelItem()
    boolVal = DescriptorModelItem()
    comboVal = DescriptorModelItem()
    sliderVal = DescriptorModelItem()
    logSliderVal = DescriptorModelItem(1)   #
    dialVal = DescriptorModelItem()
    radioVal = DescriptorModelItem()
    lineVal = DescriptorModelItem()
    colorVal = DescriptorModelItem()
    lcdVal = DescriptorModelItem()
    labelVal = DescriptorModelItem()
    gbTitle = DescriptorModelItem()

    # these initializations are optional but usually desired.  Without them the attributes will still exist
    # but will be initialized to None
    def __init__(self):
        super().__init__()
        self.numericVal = 7
        self.boolVal = True

    def summarize(self):
        summaryLines = []
        for attr in self._itemNames.values():
            summaryLines.append('{} = {}'.format(attr, getattr(self, attr)))
        return '\n'.join(summaryLines)


# first thing's first, create the QApplication
app = QApplication([])

# this works... but we don't we can't load fonts from the 'resources' ( where you specify :/ in the filename )
# without building a .qrc file and then compiling it with pyrcc4 to a .py file that can be imported
ret = QFontDatabase.addApplicationFont('/Users/christophermaierle/U20/trader20/python/qtUtils/examples/AndroidRobot-A9Kx.ttf')
font = QFont('ANDROID ROBOT')
QApplication.setFont(font)

# here's our data
model = OurDataModel()

# here's widgets that we'll use to control the data
# we'll put them all into a layout
layout = QVBoxLayout()

printButton = QPushButton('Print Data')
textArea = QTextEdit()
printButton.clicked.connect(lambda: textArea.append(model.summarize() + '\n\n'))
layout.addWidget(printButton)
layout.addWidget(textArea)
sep = QFrame()
sep.setFrameShape(QFrame.HLine)
sep.setFrameShadow(QFrame.Sunken)
layout.addWidget(sep)

sb = QSpinBox()
layout.addWidget(sb)

b = QCheckBox()
layout.addWidget(b)

rb = QRadioButton()
layout.addWidget(rb)

le = QLineEdit()
le.setReadOnly(True)
layout.addWidget(le)

s = QSlider(Qt.Horizontal)
layout.addWidget(s)

ls = LogSliderWidget(Qt.Horizontal)
layout.addWidget(ls)

d = QDial()
d.setWrapping(True)
layout.addWidget(d)

cb = QComboBox()
cb.insertItems(0, ['a', 'b', 'c', 'd'])
layout.addWidget(cb)

c = ColorButton()
layout.addWidget(c)

lb = QLabel()
layout.addWidget(lb)

gb = QGroupBox()
#gb.setCheckable(True)
gb.setLayout(QVBoxLayout())
gb.setTitle('GB title')
gb.layout().addWidget(QLabel('here is something in a box'))
layout.addWidget(gb)


pb = QPushButton('KINETIC ENERGY:')

font = QFont('ANDROID ROBOT')
QApplication.setFont(font)

def setFont():
    font = QFontDialog.getFont()
    pb.setFont(font[0])
pb.clicked.connect(setFont)
layout.addWidget(pb)


ql = QLCDNumber()
layout.addWidget(ql)
for i in range(ql.metaObject().propertyCount()):
    print(ql.metaObject().property(i).name())

# custom implementation for non-working widgets:  if you specify a property, data will get set
# by widget.setProperty(property, data)
# so... we just need that part to work


# now here's the magic.  Map widgets to model using mapper.  All of these lines are super important
# don't forget any of them.  Especially not mapper.toFirst()
mapper = ExtDataWidgetMapper()
mapper.setOrientation(Qt.Vertical)  # AbstractDescriptorModel internally uses a 'vertical' arrangement
mapper.setModel(model)

mapper.addMapping(sb, OurDataModel.numericVal.section)
mapper.addMapping(b, OurDataModel.boolVal.section)
mapper.addMapping(rb, OurDataModel.radioVal.section)
mapper.addMapping(le, OurDataModel.lineVal.section)
mapper.addMapping(s, OurDataModel.sliderVal.section)
mapper.addMapping(ls, OurDataModel.logSliderVal.section)
mapper.addMapping(d, OurDataModel.dialVal.section, b'value')
mapper.addMapping(cb, OurDataModel.comboVal.section, b'currentText')
mapper.addMapping(ql, OurDataModel.lcdVal.section, b'value')
mapper.addMapping(lb, OurDataModel.labelVal.section)
mapper.addMapping(gb, OurDataModel.gbTitle.section, b'title')
mapper.toFirst()    # call this AFTER setting up the mappings in order to sync data from the model to the gui

# NOTE:  note that the gui will not show the same value as the model when the model values are out of range for
# the gui widgets.  This can happen when ranges are exceeded or when a value is not allowed for a QComboBox, etc...

# create a console so that we can show that programatically changing a variable
# changes the GUI.  Push
console = ConsoleWidget()
console.push_vars({'model': model})

mainLayout = QHBoxLayout()
mainLayout.addLayout(layout)
mainLayout.addWidget(console)

# create our main window
win = QWidget()
win.setLayout(mainLayout)
win.move(200, 100)
win.resize(600, 400)
win.show()
win.raise_()

# and finally start the Qt event loop
QApplication.instance().exec_()


