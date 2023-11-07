from django.urls import path
from . import views
	
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('questions/', views.question_list, name='question_list'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('questions/create/', views.QuestionCreate.as_view(), name='question_create'),
    path('question/<int:pk>/update/', views.QuestionUpdate.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionDelete.as_view(), name='question_delete'),
    # path('question/<int:question_id>/comment/create/', views.CommentCreate.as_view(), name='comment_create'),
    # path('comment/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    # path('comment/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    # path('questions/<int:question_id>/add_comment/', views.add_comment, name='add_comment'),
    path('questions/<int:question_id>/comment_create/', views.add_comment, name='comment_create'),
    path('questions/<int:question_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('questions/<int:question_id>/edit_comment/', views.edit_comment, name='edit_comment'),
    
    path('accounts/signup', views.signup, name='signup')
    ]