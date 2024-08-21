from django.contrib import admin
from .models import Question, Choice

admin.site.register(Question) # Register Question model
admin.site.register(Choice) # Register Choice model