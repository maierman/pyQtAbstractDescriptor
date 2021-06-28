This directory contains code which shows a simple example of how to use the AbstractDescriptorModel class.

AbstractDescriptorModel is a model class for the pyqt model/view programming framework.   Its particular
focus is on making it easy to create a model class which:
    A) works with QDataWidgetMapper to make arbitrary two-way connections with standard QWidgets
    B) makes data read/write accessible as standard python attributes via 'dot syntax' while of course
           maintaining synchronization with any gui widgets which may be mapped

There are two demos here.  simpleDemo.py displays a bunch of widgets and hooks them up to descriptor attributes in the object
'model'  In the right hand section of the gui there is a iPython terminal where you can view and set the data attributes.  This
is simply a demo of how the gui is synced to the attributes.

The other demo is starSimulation/starSimulation.py.  This sets up a graphical simulation system of 'stars' and 'planets' 
where the planets 'orbit' around
the stars.  The attractive forces between the planets and stars can be adjusted and the stars themselves
can be created and moved about.  Graphics is mainly done via pyqtgraph and the real time graphical animation
is driven by a QTimer event.  Code organization is as follows:

starSimulation.py     -- main python (executable) script.
models.py             -- contains data models
widgets.py            -- contains custom widgets which are gui elements for display and interaction with the models
gui.py                -- creates the main gui window

## Setup

Create a virtual environment and install necessary packages.
```
virtualenv abstractdescriptor
source abstractdescriptor/bin/activate
pip install --upgrade pip setuptools wheel
pip install numpy pyside6 scipy pyqtgraph qtpy pyqt5-tools
```
Run the following command to start the simulation
`python starSimulation/starSimulation.py`
