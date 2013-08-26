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


__doc__ = """swapinfo -m
Determine memory and swap from the result of the swapinfo -m
command.
"""

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap

class memory(CommandPlugin):

    maptype = "FileSystemMap"
    compname = "os"
    command = '/usr/sbin/swapinfo'
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"


    def process(self, device, results, log):
        """Collect command-line information from this device"""
        log.info("Processing the uname -a info for device %s" % device.id)

	rm = self.relMap()
        maps = []

	output = results.split('\n')
	maps.append(ObjectMap({"totalMemory": int(output[4].split()[1])}, compname="hw"))
	maps.append(ObjectMap({"totalSwap": int(output[2].split()[1])}, compname="os"))
	
        return maps
