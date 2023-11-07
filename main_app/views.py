from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView

from .models import Question, Comment
from .forms import QuestionForm, CommentForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {
        'questions': questions
    })

@login_required
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = Comment.objects.filter(question=question)
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'comments': comments
    })

class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm

class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = '/questions'

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = '__all__'

    def form_valid(self, form):
        question = get_object_or_404(Question, pk=self.kwargs['question_id'])
        form.instance.author = self.request.user
        form.instance.question = question
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('question_detail', kwargs={'question_id': self.kwargs['question_id']})

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse('question_detail', kwargs={'question_id': self.object.question.id})