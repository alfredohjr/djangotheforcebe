from django.contrib import admin

from job.models import Crontab, ExecutionManual, Script, Group
# Register your models here.

class ScriptAdmin(admin.ModelAdmin):

    list_display = ('name','description','active')
    list_filter = ['active']


class CrontabAdmin(admin.ModelAdmin):
    
    list_display = ('name','script','minute','hour','dayOfMonth','month','dayOfWeek','active')


admin.site.register(Crontab, CrontabAdmin)
admin.site.register(Script, ScriptAdmin)
admin.site.register(ExecutionManual)
admin.site.register(Group)