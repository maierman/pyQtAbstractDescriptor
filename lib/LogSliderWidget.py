from qtpy.QtWidgets import QSlider
from qtpy.QtCore import Property
import math


class LogSliderWidget(QSlider):
    """Reimplements QSlider but makes the slider scale logarithmically over its range.  Calling
    setRange with a minimum less than or equal to zero will result in an error"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.a = None
        self.b = None
        self.setRange(1, 100)   # we choose a random default range just so that a and b get set away from None

    def setRange(self, min, max):
        # internally, QSlider will have a range of 0 - 100, but we will override value and setValue
        # to return values v(x) = a*exp(b*x) where a, b are set so that v(0) = min and v(100) = max
        if min <= 0 or min >= max:
            raise ValueError('min range must be greater than zero and less than max')
        self.a = min
        self.b = math.log(max/min) / 100
        super().setRange(0, 100)

    # we're overriding the builtin Qt property here to do our special transformations
    @Property(float, user=True)
    def value(self):
        return self.a * math.exp(self.b * super().value())

    @value.setter
    def value(self, val):
        super().setValue(math.log(val/self.a) / self.b)
