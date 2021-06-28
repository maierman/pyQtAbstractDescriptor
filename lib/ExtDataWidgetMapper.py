from qtpy.QtWidgets import QDataWidgetMapper, QCheckBox, QRadioButton, QSlider, QComboBox, QDial


class ExtDataWidgetMapper(QDataWidgetMapper):
    """This class exists because QDataWidgetMapper doesn't map QCheckBox properly to a data model.
    The reason for this is that QDataWidgetMapper relies on its delegate (QStyledItemDelegate by
    default) to emit the signal commitData when editing is finished.  Unfortunately,
    QStyledItemDelegate doesn't emit this signal for all widgets such as, for example QCheckBox
    and so we handle these widgets by manually triggering the commitData signal to emit from
    our delegate when one of these unhandled widgets updates.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def addMapping(self, widget, section, property=None):
        if isinstance(widget, (QCheckBox, QRadioButton)):
            widget.toggled.connect(lambda: self.itemDelegate().commitData.emit(widget))
        elif isinstance(widget, QSlider):
            widget.valueChanged.connect(lambda: self.itemDelegate().commitData.emit(widget))
        elif isinstance(widget, QDial):
            widget.valueChanged.connect(lambda: self.itemDelegate().commitData.emit(widget))
        elif isinstance(widget, QComboBox):
            widget.currentTextChanged.connect(lambda: self.itemDelegate().commitData.emit(widget))

        if property is not None:
            super().addMapping(widget, section, property)
        else:
            super().addMapping(widget, section)

    def setItemDelegate(self, delegate):
        # after calling super().setItemDelegate, we need to find all of the QCheckBox
        # widgets and connect them to the new delegate.  Also we should disconnect from
        # the old one.  How do we find the list of mapped widgets?
        raise NotImplementedError('FIXME:  implement this call')