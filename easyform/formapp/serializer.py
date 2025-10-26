from rest_framework import serializers
from .models import Question, Form,Choice


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

    