from qtpy.QtWidgets import QPushButton, QStyle, QColorDialog, QStylePainter, QStyleOptionButton
from qtpy.QtCore import Signal, Qt, Property
from qtpy.QtGui import QPainter, QBrush, QColor
import numpy as np


class ColorButton(QPushButton):
    """
    **Bases:** QtGui.QPushButton

    Button displaying a color and allowing the user to select a new color.  Shamelessly
    based on from pyqtgraph.widgets.ColorButton

    ====================== ============================================================
    **Signals:**
    sigColorChanging(self) emitted whenever a new color is picked in the color dialog
    sigColorChanged(self)  emitted when the selected color is accepted (user clicks OK)
    ====================== ============================================================
    """
    sigColorChanging = Signal(object)  ## emitted whenever a new color is picked in the color dialog
    sigColorChanged = Signal(object)  ## emitted when the selected color is accepted (user clicks OK)

    def __init__(self, parent=None, color=(128, 128, 128)):
        QPushButton.__init__(self, parent)
        self.setColor(color)
        self.colorDialog = QColorDialog()
        self.colorDialog.setOption(QColorDialog.ShowAlphaChannel, True)
        self.colorDialog.setOption(QColorDialog.DontUseNativeDialog, True)
        self.colorDialog.currentColorChanged.connect(self.dialogColorChanged)
        self.colorDialog.rejected.connect(self.colorRejected)
        self.colorDialog.colorSelected.connect(self.colorSelected)
        # QtCore.QObject.connect(self.colorDialog, QtCore.SIGNAL('currentColorChanged(const QColor&)'), self.currentColorChanged)
        # QtCore.QObject.connect(self.colorDialog, QtCore.SIGNAL('rejected()'), self.currentColorRejected)
        self.clicked.connect(self.selectColor)
        self.setMinimumHeight(15)
        self.setMinimumWidth(15)

    def paintEvent(self, ev):
        p = QStylePainter(self)
        option = QStyleOptionButton()
        option.initFrom(self)
        p.drawControl(QStyle.CE_PushButton, option)
        # QPushButton.paintEvent(self, ev)
        # p = QPainter(self)
        # rect = self.rect()#.adjusted(6, 6, -6, -6)
        # ## draw white base, then texture for indicating transparency, then actual color
        # p.setBrush(QBrush(QColor(255, 255, 255, 255)))
        # p.drawRect(rect)
        # p.setBrush(QBrush(Qt.DiagCrossPattern))
        # p.drawRect(rect)
        # p.setBrush(QBrush(self._color))
        # p.drawRect(rect)
        # p.end()

    def setColor(self, color, finished=True):
        """Sets the button's color and emits both sigColorChanged and sigColorChanging."""
        self._color = self.mkColor(color)
        self.update()
        if finished:
            self.sigColorChanged.emit(self)
        else:
            self.sigColorChanging.emit(self)

    def selectColor(self):
        self.origColor = self.color
        self.colorDialog.setCurrentColor(QColor(*self.color))
        self.colorDialog.open()

    def dialogColorChanged(self, color):
        if color.isValid():
            self.setColor(color, finished=False)

    def colorRejected(self):
        self.setColor(self.origColor, finished=False)

    def colorSelected(self, color):
        self.setColor(self._color, finished=True)

    @staticmethod
    def mkColor(args):
        if isinstance(args, QColor):
            return args
        elif len(args) == 3:
            (r, g, b) = args
            a = 255
        elif len(args) == 4:
            (r, g, b, a) = args
        else:
            raise RuntimeError('unhandled args to mkColor')

        args = [r, g, b, a]
        args = [0 if np.isnan(a) or np.isinf(a) else a for a in args]
        args = list(map(int, args))
        return QColor(*args)

    @Property(tuple, user=True)
    def color(self):
        color = self._color
        return (color.red(), color.green(), color.blue(), color.alpha())

    @color.setter
    def color(self, val):
        self._color = self.mkColor(val)

    # def widgetGroupInterface(self):
    #     return (self.sigColorChanged, ColorButton.saveState, ColorButton.restoreState)