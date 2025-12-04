from rest_framework import serializers
from .models import Question, Form,Choice, Responses,ReponseAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        exclude = ["created_at", "updated_at"]

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        exclude= ["created_at", "updated_at"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.question_type.lower() not in ("multiple choice", "checkboxes"):
            data.pop("choices", None)  
        return data
        
class FormSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Form
        exclude= ["created_at", "updated_at", "creator", "id"]

    
class ResponseAnwerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReponseAnswer
        fields = "__all__"    

    def to_representation(self, instance):
        data ={
            "answer": instance.answer,
            "answer_to":{
                "question" : instance.answer_to.question,
                "question_type" : instance.answer_to.question_type
            }
        }
        return data


class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responses
        exclude= ["created_at", "updated_at"]
    
    def to_representation(self, instance):
        data ={
            "code": instance.code,
            "responder_email": instance.responder_email,
            "form": {
                "code": instance.form.code,
                "title": instance.form.title
            },
            "answers": ResponseAnwerSerializer(instance.responses.all(), many= True).data
        }
        return data





class FormResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        exclude = ["created_at", "updated_at", "creator", "id"]

    def to_representation(self, instance):
        queryset = Responses.objects.filter(form=instance)
        data = {
            "code": instance.code,
            "title": instance.title,
            "background_color": instance.background_color,
            "responses": ResponsesSerializer(queryset, many=True).data
        }
        return data








