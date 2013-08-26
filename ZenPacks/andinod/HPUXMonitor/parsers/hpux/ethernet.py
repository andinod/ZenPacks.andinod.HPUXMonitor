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

# Because NICs are monitoring using Components is necesary the ComponentCommandParser

from Products.ZenRRD.ComponentCommandParser import ComponentCommandParser

class ethernet(ComponentCommandParser):

    # Filling th variables
    # How the results will be splited
    
    componentSplit = '\n'

    # Where in the line the component will be identified
    componentScanner = '(?P<component>\w+)'

    # Scan rules with Regular Expressions to extract the datapoints
    # Identified by groups.
    scanners = [
        r'\.[0-9]\d+\s+(?P<ipkts>\d+) +(?P<ierrs>\d+) +(?P<opkts>\d+) +(?P<oerrs>\d+)'
        ]

    #componentScanValue = 'Name'
