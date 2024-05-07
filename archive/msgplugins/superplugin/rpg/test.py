# -*- coding: UTF8 -*-

import django_setup

from rpg.rpg_action import *

move_acton = RpgMoveAction("123")

print(move_acton.move_down())
