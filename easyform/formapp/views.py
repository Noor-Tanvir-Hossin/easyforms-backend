from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question,Form,Responses,ReponseAnswer,Choice
from .serializer import QuestionSerializer, FormSerializer,ResponsesSerializer, FormResponseSerializer
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

class FormResponsesAPI(APIView):
    def get(self, request, pk):
        queryset = Form.objects.get(code=pk)
        serializer = FormResponseSerializer(queryset)
        
        return Response({
            'status': status.HTTP_200_OK,
            "message" : "Responses fetched successfully",
            "data": serializer.data 
        })
    

class StoreResponseAPI(APIView):
    def post (self, request):
        data= request.data
        with transaction.atomic():
            if data.get('form_code') is None or data.get('responses') is None:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    "message" : "Form code and responses both are required",
                    "data": {} 
                })
            responses = data.get('responses')
            response_obj= Responses.objects.create(
                form= Form.objects.get(code=data.get('form_code')),
                responder_email= data.get('responder_email')
            )
            for response in responses:
                question = Question.objects.get(id=response.get('question_id'))
                for answer in response['answer']:
                    if question.question_type.lower() in ["long answer", "short answer"]:
                        answer_obj= ReponseAnswer.objects.create(
                        answer= answer,
                        answer_to= question
                    )
                    else:
                        answer_obj= ReponseAnswer.objects.create(
                        answer= Choice.objects.get(id=answer).choice,
                        answer_to= question
                    )



                    
                    response_obj.responses.add(answer_obj)



            return Response({
                'status': status.HTTP_200_OK,
                "message" : "Your response has been recorded successfully",
                "data": {} 
            })
        
        return Response({
                'status': False,
                "message" : "something went wrong",
                "data": {} 
            })