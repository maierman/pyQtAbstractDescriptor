from AbstractDescriptorModel import AbstractDescriptorModel, DescriptorModelItem


# This holds 'Star' data which is just the star position.  To use DescriptorModelItem, you just
# put instances in at class level.  DescriptorModelItem is a descriptor which will allow for access
# via dot syntax as seen below in the __init__ function.
class StarModel(AbstractDescriptorModel):
    x = DescriptorModelItem()
    y = DescriptorModelItem()

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y


# and here is the main control data.  We won't even use an __init__ with this one and instead
# will just initialize at the class level by supplying the optional initialization argument to
# DescriptorModelItem.
class ControlModel(AbstractDescriptorModel):
    k = DescriptorModelItem(0.01)
    k_pow = DescriptorModelItem(1.5)
    numPlanets = DescriptorModelItem(250)
    rainbow = DescriptorModelItem(False)

