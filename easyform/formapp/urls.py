from django.urls import path

from .views import QuestionAPI,FormAPI

urlpatterns = [
    path('get-questions/', QuestionAPI.as_view(), name='get-questions'),
    path('form/<pk>', FormAPI.as_view(), name='form')
]
