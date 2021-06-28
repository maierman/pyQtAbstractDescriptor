from qtpy.QtWidgets import QLCDNumber
from qtpy.QtCore import Qt


class LCDNumberView(QLCDNumber):
    """This class facilitates connecting an integer LCD number display to a model"""
    def __init__(self, *args, integerDisplay=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.integerDisplay = integerDisplay
        self.model = None
        self.row = None
        self.col = None

    def setModel(self, model, row, column=0):
        if self.model is not None:
            self.model.dataChanged.disconnect(self.onDataChanged)
        self.model = model
        self.row = row
        self.col = column
        self.model.dataChanged.connect(self.onDataChanged)
        self.display(model.data(model.createIndex(self.row, self.col, None), Qt.DisplayRole))

    def onDataChanged(self, index1, index2):
        if index1.row() == self.row and index1.column() == self.col:
            if self.integerDisplay:
                self.display(int(index1.data()))
            else:
                self.display(index1.data())

