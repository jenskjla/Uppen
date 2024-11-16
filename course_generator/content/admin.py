# content/admin.py

from django.contrib import admin
from .models import CodingLesson, CodingExercise

@admin.register(CodingLesson)
class CodingLessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty', 'created_at')
    search_fields = ('title', 'description', 'chroma_document_id')
    list_filter = ('difficulty',)

@admin.register(CodingExercise)
class CodingExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'prompt', 'created_at')
    search_fields = ('prompt', 'starter_code', 'solution_code', 'hints')
    list_filter = ('lesson',)
