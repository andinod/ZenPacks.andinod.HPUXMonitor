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


__doc__ = """lanscan
lanscan and netstat  maps the interfaces relation.
"""

import re

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class lanscan(CommandPlugin):
    # echo __COMMAND__ is used to delimit the results
    command = '/usr/bin/netstat -in && echo __COMMAND__ && /usr/sbin/lanscan'
    compname = "os"
    relname = "interfaces"
    modname = "Products.ZenModel.IpInterface"
    deviceProperties = CommandPlugin.deviceProperties + (
           'zInterfaceMapIgnoreNames', 'zInterfaceMapIgnoreTypes')

    def process(self, device, results, log):

        log.info('Modeler %s processing data for device %s', self.name(), device.id)
        self.log = log
	
	# split the results of the 2 commands with our token __COMMAND__
        netstat, lanscan = results.split('__COMMAND__')
	
	#Calling function parseIfconfig to get the related information
        relMap = self.parseIfconfig(netstat, lanscan, device, self.relMap())
        return relMap
        
    def parseIfconfig(self, netstat, lanscan, device, relMap):
        """
        Parse the output of the two commands netstat and  lanscan for macaddresses.
        """
	# spliting lines for netstat
	rlines = netstat.splitlines()
	# spliting lines for macs but in fact is all the hardware information getting through lanscan
	macs = lanscan.splitlines()

        iface = None
        for line in rlines:

		# Excluding interface lo0 and headers
		# Only execute for active interfaces
		if line.find('Name') != 0 and line.find('lo0') != 0:
			iface = None
			data = line.split()

			# According to this data has to be a list with this information:
			# data[0] Interface Name
			# data[1] MTU
			# data[2] Network
			# data[3] Address
			# data[4] Ipkts
			# data[5] Ierrs
			# data[6] Opkts
			# data[7] Oerrs
			# data[8] Coll

			if data[3].find('none') != 0:
				iface = self.objectMap()
				
				# Filtering our NIC in lanscan table
				ilanscan = filter(lambda x: data[0].strip() in x,macs)[0]
				# Looking for type
				itype = ilanscan.split()[7].strip()
				if "ETHER" in itype: 
					itype="HPUXEthernet"
				iface.type = itype	
				iface.interfaceName = data[0].strip()
				iface.id = self.prepId(data[0].strip())
				iface.macaddress = ilanscan.split()[1].strip()

				# For description we will display Hardware Path Information
				iface.description = ilanscan.split()[0].strip()

				dontCollectIntNames = getattr(device, 'zInterfaceMapIgnoreNames', None)
				if dontCollectIntNames and re.search(dontCollectIntNames, iface.interfaceName):
					self.log.debug("Interface %s matched the zInterfaceMapIgnoreNames zprop '%s'",
						iface.interfaceName, dontCollectIntNames)
					continue
				dontCollectIntTypes = getattr(device, 'zInterfaceMapIgnoreTypes', None)
				if dontCollectIntTypes and re.search(dontCollectIntTypes, iface.type):
                    			self.log.debug("Interface %s type %s matched the zInterfaceMapIgnoreTypes zprop '%s'",
                      				iface.interfaceName, iface.type, dontCollectIntTypes)
                    			continue

				relMap.append(iface)

				if not hasattr(iface, 'setIpAddresses'):
					iface.setIpAddresses = []
				iface.setIpAddresses.append("%s" % (data[3].strip()))
				# get the state UP/DOWN of the interface
				# lanscan's output contains information about the state of the NIC
				flags = ilanscan.split()[3]
				mtu = data[1].strip()

				if "UP" in flags: iface.operStatus = 1
				else: iface.operStatus = 2
				
				iface.mtu = mtu
				iface.adminStatus = 1

	
	return relMap	
