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


__doc__ = """bdf
Determine the filesystems to monitor
"""

import re

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

class bdf(CommandPlugin):
    """
    Run bdf to model filesystem information. Should work on every HP-UX servers
    """
    maptype = "FilesystemMap" 
    command = '/usr/bin/bdf'
    compname = "os"
    relname = "filesystems"
    modname = "Products.ZenModel.FileSystem"
    deviceProperties = \
                CommandPlugin.deviceProperties + ('zFileSystemMapIgnoreNames',)

    oses = ['HP-UX']

    def condition(self, device, log):
        return device.os.uname == '' or device.os.uname in self.oses


    def process(self, device, results, log):
        log.info('Collecting filesystems for device %s' % device.id)
        skipfsnames = getattr(device, 'zFileSystemMapIgnoreNames', None)
        rm = self.relMap()
        rlines = results.split("\n")
        bline = ""
        for line in rlines:
            if line.startswith("Filesystem"): continue
            om = self.objectMap()
            spline = line.split()
            if len(spline) == 1:
                bline = spline[0]
                continue
            if bline: 
                spline.insert(0,bline)
                bline = None
            if len(spline) != 6: continue
            (om.storageDevice, tblocks, u, a, p, om.mount) = spline
            if skipfsnames and re.search(skipfsnames,om.mount): continue

            if tblocks == "-":
                om.totalBlocks = 0
            else:
                try:
                    om.totalBlocks = long(tblocks)
                except ValueError:
                    # Ignore this filesystem if what we thought was total
                    # blocks isn't a number.
                    continue

            om.blockSize = 1024
            om.id = self.prepId(om.mount)
            om.title = om.mount
            rm.append(om)
        return rm
