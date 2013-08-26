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
    command = "uname -a && echo __COM__ && /sbin/getconf MACHINE_SERIAL && echo __COM__ && /usr/bin/uptime | /sbin/awk '{print $3, $4}' && echo __COM__ && /usr/bin/model"

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

	# Second Hardware Serial
	om.serialNumber = data[1].strip('\n')

	# Third Uptime	
	om.uptime = data[2].strip('\n,')
	
	# Fourth model
	provider,type,model=data[3].split()[1:]
	om.setHWProductKey = " ".join([provider,model])
	log.debug("Hardware Model=%s Serial=%s Uptime=%s"  % (om.setHWProductKey, om.serialNumber, om.uptime))
	
        return om
