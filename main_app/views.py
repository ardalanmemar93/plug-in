import os
import uuid
import boto3
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from markdownx.utils import markdownify


from .models import Question, Comment, Photo, MarkedDownExample 
from .forms import QuestionForm, CommentForm, MarkedDownExampleForm

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


class MarkdownDetailView(DetailView):
    model = MarkedDownExample
    template_name = 'questions/question_detail.html'  
    
def question_detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    comments = Comment.objects.filter(question=question)
    # Fetch the MarkedDownExample instance separately
    try:
        # markdown_example = MarkedDownExample.objects.get(question=question)
        # Convert Markdown content to HTML using markdownx.utils.markdownify
        markdown_html = markdownify(question.content)
    except Exception as e:
        print(e)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            if 'comment_id' in request.POST:
                comment_id = request.POST['comment_id']
                existing_comment = get_object_or_404(Comment, pk=comment_id)
                if existing_comment.author == request.user:
                    existing_comment.content = comment_form.cleaned_data['content']
                    existing_comment.save()
            else:
                new_comment = comment_form.save(commit=False)
                new_comment.author = request.user
                new_comment.question = question
                new_comment.save()
            return redirect('question_detail', question_id=question.id)
    else:
        comment_form = CommentForm()
    return render(request, 'questions/question_detail.html', {
        'question': question,
        'comments': comments,
        'comment_form': comment_form,
        # 'markdown_example': markdown_example,
        'markdown_html': markdown_html,
    })
    
    
    

# @login_required
# def question_detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     comments = Comment.objects.filter(question=question)

#     # Fetch the MarkedDownExample instance separately
#     try:
#         # markdown_example = MarkedDownExample.objects.get(question=question)
#         # Convert Markdown content to HTML using markdownx.utils.markdownify
#         markdown_html = markdownify(question.content)
#         print(markdown_html)
#     except Exception as e:
#         print(e)
       

#     return render(request, 'questions/question_detail.html', {
#         'question': question,
#         'comments': comments,
#         'comment_form': CommentForm(),
#         # 'markdown_example': markdown_example,
#         # 'markdown_html': markdown_html,
#     })





# @login_required
# def question_detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     comments = Comment.objects.filter(question=question)
    
#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             if 'comment_id' in request.POST:  # Check if 'comment_id' is in the POST data
#                 # This means it's an edit
#                 comment_id = request.POST['comment_id']
#                 existing_comment = get_object_or_404(Comment, pk=comment_id)
#                 if existing_comment.author == request.user:
#                     # Check if the user is the author of the existing comment
#                     existing_comment.content = comment_form.cleaned_data['content']
#                     existing_comment.save()
#             else:
#                 new_comment = comment_form.save(commit=False)
#                 new_comment.author = request.user
#                 new_comment.question = question
#                 new_comment.save()
#             return redirect('question_detail', question_id=question.id)
#     else:
#         comment_form = CommentForm()

#     return render(request, 'questions/question_detail.html', {
#         'question': question,
#         'comments': comments,
#         'comment_form': comment_form
#     })



class QuestionCreate(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    success_url = '/questions'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class QuestionUpdate(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionForm

class QuestionDelete(LoginRequiredMixin, DeleteView):
    model = Question
    success_url = '/questions'
    

@login_required
def add_comment(request, question_id):
    if request.method == 'POST':
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

    # Check if the user is the author of the comment
    if request.user == comment.author:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('question_detail', question_id=comment.question.id)
        else:
            form = CommentForm(instance=comment)

        return render(request, 'main_app/comment_form.html', {'form': form, 'comment': comment})
    else:
        return HttpResponseForbidden("You are not allowed to edit this comment.")

    
    
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        if request.method == 'POST':
            comment.delete()
            return redirect('question_detail', question_id=comment.question_id)
        return render(request, 'main_app/delete_comment.html', {'comment': comment})
    else:
        return HttpResponseForbidden("You are not allowed to delete this comment.")
   


@login_required
def add_photo(request, question_id):
    photo_file = request.FILES.get('photo_file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            print(f"Uploading file to S3. Bucket: {bucket}, Key: {key}")
            # Upload the file to S3
            s3.upload_fileobj(photo_file, bucket, key)
            print("File uploaded successfully to S3")
            # Construct the URL
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            print(f"Generated URL: {url}")
            # Create a Photo object
            Photo.objects.create(url=url, question_id=question_id)
            print("Photo object created successfully")
        except Exception as e:
            print('An error occurred uploading a file to S3')
            print(e)
    else:
        print("No photo file provided in the request")
    # Redirect to question detail page
    return redirect('question_detail', question_id=question_id)


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