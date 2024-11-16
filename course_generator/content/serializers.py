# content/serializers.py

from rest_framework import serializers
from .models import CodingLesson, CodingExercise, StudentInteraction, CommonQuestion, StruggleAnalysis

class CodingExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingExercise
        fields = ['id', 'lesson', 'prompt', 'starter_code', 'solution_code', 'hints', 'created_at']
        read_only_fields = ['id', 'created_at']


class StudentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInteraction
        fields = ['id', 'lesson', 'exercise', 'question', 'response', 'timestamp', 'helpful']
        read_only_fields = ['id', 'timestamp']


class CommonQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonQuestion
        fields = ['id', 'lesson', 'question', 'frequency']
        read_only_fields = ['id']


class StruggleAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StruggleAnalysis
        fields = ['id', 'lesson', 'topic', 'frequency']
        read_only_fields = ['id']


class CodingLessonSerializer(serializers.ModelSerializer):
    exercises = CodingExerciseSerializer(many=True, read_only=True)
    interactions = StudentInteractionSerializer(many=True, read_only=True)
    common_questions = CommonQuestionSerializer(many=True, read_only=True, source='common_questions_set')
    struggle_topics = StruggleAnalysisSerializer(many=True, read_only=True, source='struggle_analyses')

    class Meta:
        model = CodingLesson
        fields = [
            'id',
            'title',
            'description',
            'chroma_document_id',
            'difficulty',
            'created_at',
            'total_interactions',
            'common_questions',
            'struggle_topics',
            'feedback_summary',
            'lecture_goals',
            'lecture_topics',
            'topic_tags',
            'exercises',
            'interactions',
        ]
        read_only_fields = ['id', 'created_at', 'total_interactions', 'common_questions', 'struggle_topics', 'feedback_summary', 'lecture_goals', 'lecture_topics', 'topic_tags', 'exercises', 'interactions']
