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

class memory(CommandParser):

	def processResults(self, cmd, result):

		# Create lookup table for datapoints
		dp_map = dict([(dp.id, dp) for dp in cmd.points])

		#import pdb; pdb.set_trace()

		# Getting all lines
		for line in cmd.result.output.split('\n'):
		
			# Ignoring unnecesary information
			if "memory" in line: 
				total, used, free = line.split()[1:4]
				result.values.append((dp_map['total'],total))
				result.values.append((dp_map['used'],used))
				result.values.append((dp_map['free'],free))

