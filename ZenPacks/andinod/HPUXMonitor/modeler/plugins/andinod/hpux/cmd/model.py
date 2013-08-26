##############################################################################
#
# Copyright (C) David Andino, CIV 138.286, Punto Fijo, Venezuela, 
# all rights reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
##############################################################################

__doc__ = """model
Determine hardware model from the result of the model
command.
"""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class model(CommandPlugin):

    maptype = "DeviceMap"
    compname = ""
    command = '/usr/bin/model'

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        om = self.objectMap()
	provider,type,model=results.split()[1:]
        om.setHWProductKey = " ".join([provider,model])
        log.debug("Hardware Model=%s"  % (om.setHWProductKey))
        return om
