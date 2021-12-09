from django.contrib import admin
from core.models import Process, Part


class PartInline(admin.StackedInline):
    model = Part
    extra = 0


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'subject', 'judge')
    search_fields = ('judge', 'subject', 'process_class')
    inlines = [PartInline, ]


admin.site.register(Process, ProcessAdmin)
