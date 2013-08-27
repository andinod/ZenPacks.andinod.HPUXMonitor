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

class systemscan(CommandPlugin):

    maptype = "DeviceMap"
    compname = ""
    command = "uname -a && echo __COM__ && /usr/bin/model"

    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)
        om = self.objectMap()
	# Split the data in tokens to analyse
	data = results.split('__COM__')
 	#import pdb; pdb.set_trace()


	# First uname results
        om.snmpDescr = data[0].strip() 
        os,om.snmpSysName, kernelRelease = data[0].split()[:3]
        om.setOSProductKey = " ".join([os, kernelRelease])
        log.debug("snmpSysName=%s, setOSProductKey=%s" % (
                om.snmpSysName, om.setOSProductKey))

	# Second model
	provider=data[1].split()[1]
	type = data[1].split()[2]
	model = data[1].split()[3]
	om.setHWProductKey = " ".join([provider,model])
	log.debug("Hardware Model=%s"   % (om.setHWProductKey))
	
        return om
