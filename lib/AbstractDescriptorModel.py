from qtpy.QtCore import QAbstractListModel
from qtpy.QtCore import Qt


class AbstractDescriptorModel(QAbstractListModel):
    """This is an abstract model which works with the Qt model view framework.  It allows the user
    to store values using simple attribute-like dot accessor syntax while also facilitating easy
    mapping of data to Qt widgets via QDataWidgetMapper.  Note that AbstractDescriptorModel is not
    intended to be used on its own but should instead be subclassed where the derived class is
    expected to have DescriptorModelItem class variables.

    For example, given the class:

    class ExampleModel(AbstractDescriptorModel):
        var1 = DescriptorModelItem()     # as always, define descriptors at CLASS level
        var2 = DescriptorModelItem()

    var1 and var2 can be accessed just as if they were simple attributes.  The attributes var1 and var2 will be
    initialized to None by default and can be explicitly initialized either by passing the initialization value
    as DescriptorModelItem(initialVal) or simply using dot accessor syntax in a derived class __init__ just as
    would be done with any other attribute.

    To map var1 and var2 to qt widgets you would do the following:

    model = ExampleModel()
    mapper = QDataWidgetMapper()
    mapper.setOrientation(Qt.Vertical)   # our data derives from the vertically oriented QAbstractListModel
    mapper.setModel(model)
    mapper.toFirst()                     # very important!  don't forget this call!!!

    w1 = QSpinBox()
    w2 = QSpinBox()
    mapper.addMapping(w1, ExampleModel.var1.section)    # map widget w1 to model.var1
    mapper.addMapping(w2, ExampleModel.var2.section)    # map widget w2 to model.var2
    """

    def __init__(self):
        super().__init__()

        # loop over all of the mro classes and find any DescriptorModelItems.
        # Then assign a 'section' id to each one and create a map of 'section' to public_name
        self._itemNames = {}
        section = 0
        for cls in type(self).mro():
            if cls is AbstractDescriptorModel:
                break   # don't need to dig into QAbstractListModel
            for attr, desc in cls.__dict__.items():
                if isinstance(desc, DescriptorModelItem):
                    desc.section = section
                    self._itemNames[desc.section] = desc.public_name
                    section += 1

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def rowCount(self, parent):
        return len(self._itemNames)

    def data(self, index, role):
        if role in [Qt.DisplayRole, Qt.EditRole]:
            return getattr(self, self._itemNames[index.row()])
        else:
            return None

    def setData(self, index, value, role):
        setattr(self, self._itemNames[index.row()], value)
        return True


class DescriptorModelItem:
    """This is a descriptor class which should be used as a class attribute to manage data access in classes
    derived from AbstractDescriptorModel.  It implements standard 'property-like' get/set infrastructure.

    The attribute 'section' is used to store an integer identifier for the data which is necessary in order
    to support data lookup via an integer as required by the Qt model view framework.  The name 'section' is
    used because this is the terminology used in QDataWidgetMapper which is the glue which can be used to
    tie models to widgets or views in Qt
    """
    def __init__(self, initialVal=None):
        self._initialVal = initialVal

    def __set_name__(self, owner, name):
        self.private_name = '_' + name
        self.public_name = name
        self.section = None    # we'll come back later and set this
        setattr(owner, self.private_name, self._initialVal)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # accessed on class, return descriptor itself
        else:
            return getattr(obj, self.private_name)

    def __set__(self, obj, val):
        # first update the data
        setattr(obj, self.private_name, val)

        # obj is intended to be derived from a model view model ( such as QAbstractItemModel ).
        # In Qt, when we set data on a model view model, we need to emit the signal dataChanged
        # to let views know that they should update.
        index = obj.createIndex(self.section, 0, None)     # tell the view what updated...
        obj.dataChanged.emit(index, index)
