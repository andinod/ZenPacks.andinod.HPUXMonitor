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


__doc__ = """uname -a
Determine snmpSysName and setOSProductKey from the result of the uname -a
command.
"""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class uname_a(CommandPlugin):

    maptype = "DeviceMap"
    compname = ""
    command = 'uname -a'

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        om = self.objectMap()
        om.snmpDescr = results.strip()
        os,om.snmpSysName, kernelRelease = results.split()[:3]
        om.setOSProductKey = " ".join([os, kernelRelease])
        log.debug("snmpSysName=%s, setOSProductKey=%s" % (
                om.snmpSysName, om.setOSProductKey))
        return om
