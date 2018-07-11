# -*- coding: UTF8 -*-

import os
import sys
import django
CURRENT_PATH = os.path.dirname(__file__)
print(CURRENT_PATH)
sys.path.append(CURRENT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superplugin.settings")
django.setup()
