# -*- coding: UTF8 -*-

import os
import sys
import django
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superplugin.settings")
django.setup()
from group.models import *
from group import GroupAction

