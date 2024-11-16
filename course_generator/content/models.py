# content/models.py

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# from .tasks import analyze_lecture_pdf  # Celery task to analyze lecture PDF

class CodingLesson(models.Model):
    """
    Represents a coding lesson, linked to a Chroma document (PDF).
    Includes fields for lecture analysis and interaction analytics.
    """
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=255, help_text="Title of the lesson.")
    description = models.TextField(help_text="Detailed description of the lesson.")
    chroma_document_id = models.CharField(
        max_length=255,
        help_text="Path or identifier linking to the Chroma document (e.g., PDF file)."
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        help_text="Difficulty level of the lesson."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the lesson was created.")

    # **Analysis Attributes**
    total_interactions = models.PositiveIntegerField(
        default=0,
        help_text="Total number of student interactions with this lesson."
    )
    common_questions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Frequently asked questions by students."
    )
    struggle_topics = models.JSONField(
        default=dict,
        blank=True,
        help_text="Topics where students commonly struggle."
    )
    feedback_summary = models.TextField(
        blank=True,
        null=True,
        help_text="Summary of student feedback and interactions."
    )

    # **Lecture Analysis Attributes**
    lecture_goals = models.TextField(
        blank=True,
        null=True,
        help_text="Goals extracted from the lecture PDF."
    )
    lecture_topics = models.JSONField(
        default=list,
        blank=True,
        help_text="List of topics covered in the lecture."
    )
    topic_tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Tags related to the lecture topics."
    )

    def __str__(self):
        return self.title


class CodingExercise(models.Model):
    """
    Represents an exercise within a coding lesson.
    """
    lesson = models.ForeignKey(
        CodingLesson,
        related_name='exercises',
        on_delete=models.CASCADE,
        help_text="The lesson this exercise belongs to."
    )
    prompt = models.TextField(help_text="The exercise prompt presented to the student.")
    starter_code = models.TextField(
        blank=True,
        null=True,
        help_text="Starter code provided to the student."
    )
    solution_code = models.TextField(
        blank=True,
        null=True,
        help_text="Solution code for the exercise."
    )
    hints = models.TextField(
        blank=True,
        null=True,
        help_text="Hints to assist the student in solving the exercise."
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the exercise was created.")

    def __str__(self):
        return f"Exercise {self.id} for {self.lesson.title}"


class StudentInteraction(models.Model):
    """
    Captures each interaction a student has with the LLM within a lesson.
    """
    lesson = models.ForeignKey(
        CodingLesson,
        related_name='interactions',
        on_delete=models.CASCADE,
        help_text="The lesson associated with this interaction."
    )
    exercise = models.ForeignKey(
        CodingExercise,
        related_name='interactions',
        on_delete=models.CASCADE,
        help_text="The exercise associated with this interaction."
    )
    question = models.TextField(help_text="The question asked by the student.")
    response = models.TextField(help_text="The LLM's response to the student's question.")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the interaction occurred.")
    helpful = models.BooleanField(
        default=True,
        help_text="Indicates if the student found the response helpful."
    )

    def __str__(self):
        return f"Interaction {self.id} for Lesson {self.lesson.title}"


class CommonQuestion(models.Model):
    """
    Tracks frequently asked questions within a lesson.
    """
    lesson = models.ForeignKey(
        CodingLesson,
        related_name='common_questions_set',
        on_delete=models.CASCADE,
        help_text="The lesson associated with this common question."
    )
    question = models.TextField(help_text="The frequently asked question.")
    frequency = models.PositiveIntegerField(
        default=0,
        help_text="How often the question was asked."
    )

    def __str__(self):
        return f"Q: {self.question[:50]}... ({self.frequency})"


class StruggleAnalysis(models.Model):
    """
    Stores analysis results identifying topics where students commonly struggle.
    """
    lesson = models.ForeignKey(
        CodingLesson,
        related_name='struggle_analyses',
        on_delete=models.CASCADE,
        help_text="The lesson associated with this struggle topic."
    )
    topic = models.CharField(max_length=255, help_text="The topic where students struggle.")
    frequency = models.PositiveIntegerField(
        default=0,
        help_text="How often students struggled with this topic."
    )

    def __str__(self):
        return f"{self.topic} ({self.frequency})"


# **Signal to Trigger Analysis After Lesson Creation**

