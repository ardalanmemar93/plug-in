from django.contrib import admin
from .models import Question, Comment, Photo

# Register your models here.
admin.site.register(Question)
admin.site.register(Comment)
admin.site.register(Photo)