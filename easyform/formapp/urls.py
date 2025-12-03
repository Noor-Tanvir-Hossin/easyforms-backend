from django.urls import path

from .views import QuestionAPI,FormAPI,StoreResponseAPI

urlpatterns = [
    path('get-questions/', QuestionAPI.as_view(), name='get-questions'),
    path('form/<pk>', FormAPI.as_view(), name='form'),
    path('store-response/', StoreResponseAPI.as_view(), name='store-response')
]
