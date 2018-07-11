from django.contrib import admin
from group.models import *
# Register your models here.

admin.site.register(GroupGlobalSetting)
admin.site.register(GroupUser)
admin.site.register(SignRecord)
admin.site.register(TransferPointRecord)
