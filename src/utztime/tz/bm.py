# --------------------------------------------------------------------- #
# Micropython Timezone Library                                          #
#                                                                       #
# Copyright (C) 2024 by Shane Powell                                    #
# Copyright (C) 2018 by Jack Christensen                                #
# licensed under GNU GPL v3.0, https://www.gnu.org/licenses/gpl.html    #
# --------------------------------------------------------------------- #

from .. import utimezone as tz

from .ca import _AST, _ADT

# Canonical Zones
Atlantic_Bermuda = tz.Timezone(std=_AST, dst=_ADT, name='Atlantic/Bermuda')
