from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
    path('edit_question/<int:question_id>/', views.edit_question, name='edit_question'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]