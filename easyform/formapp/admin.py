from django.contrib import admin

from .models import Choice,Question, Form,ReponseAnswer,Responses



admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Form)

admin.site.register(Responses)
admin.site.register(ReponseAnswer)