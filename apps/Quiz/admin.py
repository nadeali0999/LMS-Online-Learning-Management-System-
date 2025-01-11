from django.contrib import admin

from apps.Quiz.models import *


class QuestionTabularInline(admin.TabularInline):
    model = Question


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionTabularInline]  # Only include QuestionTabularInline


admin.site.register(UserAnswer)
admin.site.register(QuizAttempt)
