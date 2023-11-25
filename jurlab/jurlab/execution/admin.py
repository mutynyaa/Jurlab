from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class CommentsExAdmin(SummernoteModelAdmin):
    summernote_fields  = ('text',)

admin.site.register(Executions)
admin.site.register(ExecutionComments, CommentsExAdmin)
admin.site.register(ExecutionDocuments)
admin.site.register(ExecutionCategory)