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

from Products.ZenRRD.CommandParser import CommandParser

class cpu(CommandParser):

	def processResults(self, cmd, result):

		# Create lookup table for datapoints
		dp_map = dict([(dp.id, dp) for dp in cmd.points])

		#import pdb; pdb.set_trace()

		# Getting all lines
		for line in cmd.result.output.split('\n'):
		
			# Ignoring unnecesary information
			if not line or "HP" in line or "usr" in line:
				continue

			hour, usr, sys, wio, idle = line.split()
	
			result.values.append((dp_map['usr'],usr))
			result.values.append((dp_map['sys'],sys))
			result.values.append((dp_map['wio'],wio))
			result.values.append((dp_map['idle'],idle))

