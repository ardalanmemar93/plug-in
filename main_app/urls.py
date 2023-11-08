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
    path('questions/<int:question_id>/comment_create/', views.add_comment, name='comment_create'),
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='comment_edit'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='comment_delete'),
    path('questions/<int:question_id>/add_photo/', views.add_photo, name='add_photo'),
    path('accounts/signup', views.signup, name='signup'),
    ]