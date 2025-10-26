from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question,Form
from .serializer import QuestionSerializer, FormSerializer
# Create your views here.

class QuestionAPI(APIView):
    def get(self, request):
        queryset = Question.objects.all()
        serializer = QuestionSerializer(queryset, many=True)
        
        return Response({
            'status': status.HTTP_200_OK,
            "message" : "Questions fetched successfully",
            "data": serializer.data 
        })
    
class FormAPI(APIView):
    def get(self, request, pk):
        queryset = Form.objects.get(code=pk)
        serializer = FormSerializer(queryset)
        
        return Response({
            'status': status.HTTP_200_OK,
            "message" : "Form fetched successfully",
            "data": serializer.data 
        })