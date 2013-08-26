from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class HPUXDevice(Device):
    """
    Example device subclass. In this case the reason for creating a subclass of
    device is to add a new type of relation. We want many "ExampleComponent"
    components to be associated with each of these devices.

    If you set the zPythonClass of a device class to
    ZenPacks.NAMESPACE.PACKNAME.ExampleDevice, any devices created or moved
    into that device class will become this class and be able to contain
    ExampleComponents.
    """

    uptime = None
    serialNumber = None

    _properties = Device._properties + ( 
	{ 'id':'serialNumber','type':'string'},
	{ 'id':'uptime','type':'string'},
    	)
