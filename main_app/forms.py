from django import forms

from .models import Question, Comment
# from .models import MarkedDownExample

# class MarkedDownExampleForm(forms.ModelForm):
#     class Meta:
#         model = MarkedDownExample
#         fields = '__all__'

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        
        # model = MarkedDownExample
        # fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Your Comment'
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }