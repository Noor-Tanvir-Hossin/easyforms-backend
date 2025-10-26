from django.contrib import admin

from .models import Choice,Question, Form

# Register your models here.

admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Form)