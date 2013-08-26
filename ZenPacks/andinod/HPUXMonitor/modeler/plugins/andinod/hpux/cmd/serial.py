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

from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin

# Classes we'll need for returning proper results from our modeler plugin's
# process method.
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


class serial(CommandPlugin):

    # The command to run.
    command = '/sbin/getconf MACHINE_SERIAL'

    def condition(self, device, log):
        return True

    def process(self, device, results, log):
        log.info("Modeler %s processing data for device %s",
            self.name(), device.id)

	serial = results.strip('\n')

        return self.objectMap({
        	'serialNumber': serial,
        	})
