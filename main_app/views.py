from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Question, Comment
from .forms import QuestionForm, CommentForm

# Create your views here.

def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})

def about(request):
  return render(request, 'about.html')

# @login_required
def profile(request):
    questions = Question.objects.filter(author=request.user)
    return render(request, 'profile.html', {'questions': questions})

@login_required
def question_list(request):
    questions = Question.objects.all()
    return render(request, 'questions/question_list.html', {
        'questions': questions
    })

# @login_required
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
    

# class CommentCreate(LoginRequiredMixin, CreateView):
#     model = Comment
#     fields = ['content', '']

#     def form_valid(self, form):
#         question = get_object_or_404(Question, pk=self.kwargs['question_id'])
#         form.instance.author = self.request.user
#         form.instance.question = question
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('question_detail', kwargs={'question_id': self.kwargs['question_id']})

# class CommentUpdate(LoginRequiredMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm

# class CommentDelete(LoginRequiredMixin, DeleteView):
#     model = Comment
#     template_name = 'comment/comment_confirm_delete.html'

#     def get_success_url(self):
#         return reverse('question_detail', kwargs={'question_id': self.object.question.id})
    
    
@login_required
def add_comment(request, question_id):
  form = CommentForm(request.POST)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.author = request.user  
    new_comment.question_id = question_id
    new_comment.save()
  return redirect('question_detail', question_id=question_id)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, isntance=comment)
            if form.is_valid():
                form.save()
                return redirect('question_detail', question_id=comment.question_id)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'comment/comment_form.html', {'form': form, 'comment': comment})
    else:
        pass
    
    
    
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        if request.method == 'POST':
            comment.delete()
            return redirect('question_detail', question_id=comment.question_id)
        return render(request, 'delete_comment.html', {'comment': comment})
    else:
        pass
   
    

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Deja Vu, try again.'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)