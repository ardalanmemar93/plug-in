from django import forms
# from ckeditor.widgets import CKEditorWidget
# from ckeditor.fields import RichTextField
from .models import Question, Comment
from .models import MarkedDownExample

class MarkedDownExampleForm(forms.ModelForm):
    class Meta:
        model = MarkedDownExample
        fields = '__all__'

class QuestionForm(forms.ModelForm):
    class Meta:
        # code = RichTextField()
        model = Question
        fields = ['title', 'content']
        # widgets = {
        #     'content': CKEditorWidget(),
        # }
        model = MarkedDownExample
        fields = '__all__'

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