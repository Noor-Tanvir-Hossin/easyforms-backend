from django.db import models
from django.contrib.auth.models import User
from rest_framework.response import Response
from .choices import QUESTION_CHOICES

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Form(BaseModel):
    code= models.CharField(max_length=10, unique=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    creator= models.ForeignKey(User, on_delete=models.CASCADE)
    background_color = models.CharField(max_length=50, default="#3f363c")
    # questions= models.ManyToManyField(Question, related_name="form_questions", blank=True)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4()).replace("-", "")[:10]
        super().save(*args, **kwargs)





class Question(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    question= models.CharField(max_length=100)
    question_type = models.CharField(max_length=100,  choices= QUESTION_CHOICES)
    required = models.BooleanField(default=True)
    # choices = models.ManyToManyField(Choice, related_name="question_choices", blank=True)

    def __str__(self):
        return self.question

class Choice(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice = models.CharField(max_length=100)
    def __str__(self):
        return self.choice



class ReponseAnswer(BaseModel):
    answer= models.CharField(max_length=100)
    answer_to= models.ForeignKey(Question, on_delete=models.CASCADE)
    def __str__(self):
        return self.answer

class Responses(BaseModel):
    code= models.CharField(max_length=10, unique=True, blank=True)
    form= models.ForeignKey(Form, on_delete=models.CASCADE)
    responder_email= models.EmailField(null = True, blank= True)
    responses= models.ManyToManyField(ReponseAnswer, related_name="response_answers")

    def __str__(self):
        return f"Response to {self.form.title} by {self.responder_email or 'Anonymous'}"
    def save(self, *args, **kwargs):
        if not self.code:
            import uuid
            self.code = str(uuid.uuid4()).replace("-", "")[:10]
        super().save(*args, **kwargs)
