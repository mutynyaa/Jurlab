from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class CommentsCourtsAdmin(SummernoteModelAdmin):
    summernote_fields  = ('text',)



admin.site.register(Courts)
admin.site.register(CourtsStatus)
admin.site.register(CourtsJudgment)
admin.site.register(CourtsCategory)
admin.site.register(CommentsCourts, CommentsCourtsAdmin)
admin.site.register(CourtDocuments)

