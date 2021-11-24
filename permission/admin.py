from django.contrib import admin
from permission.models import Permission, GroupPermission, UserGroup, Group
# Register your models here.

admin.site.register(Permission)
admin.site.register(GroupPermission)
admin.site.register(UserGroup)
admin.site.register(Group)