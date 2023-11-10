from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Question(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"question_id": self.id})
    

class Comment(models.Model):
    content = models.TextField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"Comment by {self.author} on '{self.content}' at {self.created_at}"
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for question_id: {self.question_id} @{self.url}"