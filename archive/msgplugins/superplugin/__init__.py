# -*- coding: UTF8 -*-
import os
import sys
from pathlib import Path

import django

CURRENT_PATH = Path(__file__).parent.parent
sys.path.append(os.path.join(CURRENT_PATH, "superplugin"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msgplugins.superplugin.superplugin.settings")
django.setup()

from group.models import *
from group.group_action import GroupAction, GroupPointAction
from account.user_action import UserAction
from globalconf.models import GlobalSetting
from globalconf.admin_action import AdminAction


__all__ = ["GroupAction", "GroupPointAction", "GroupUser",
           "UserAction", "GlobalSetting", "GroupGlobalSetting", "AdminAction"]
