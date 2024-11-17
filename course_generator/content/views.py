# content/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CodingLesson, CodingExercise, StudentInteraction, CommonQuestion, StruggleAnalysis
from .serializers import (
    CodingLessonSerializer,
    CodingExerciseSerializer,
    StudentInteractionSerializer,
    CommonQuestionSerializer,
    StruggleAnalysisSerializer
)
from django.http import JsonResponse
from django.conf import settings
import os
import logging
import json
import requests
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI

# Configure logger
logger = logging.getLogger(__name__)

# Constants (Adjust these as needed)
CHROMA_PATH = os.path.join(settings.BASE_DIR, 'chroma')
PROMPT_TEMPLATE = """
Analyze the following lecture notes and extract the goals, topics covered, and relevant tags. Provide the information in a valid JSON format with the following keys: "lecture_goals", "lecture_topics", and "topic_tags".

Context:
{context}

Lecture Notes:
{question}
"""

# Securely retrieve API key from environment variables
LLM_API_KEY = os.getenv('OPENAI_API_KEY')  # Ensure this is set in your environment

class LectureViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='process-lecture')
    def process_lecture(self, request):
        # 1. Retrieve and process input data
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 2. Save the uploaded file temporarily
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file.name)
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        with open(pdf_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        
        # 3. Extract text from PDF
        text_content = self.extract_text_from_pdf(pdf_path)
        if not text_content:
            return Response({"error": "Failed to extract text from the PDF."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Optionally, remove the file after processing
        try:
            os.remove(pdf_path)
        except Exception as e:
            logger.warning(f"Failed to remove temporary file {pdf_path}: {str(e)}")
        
        # 4. Perform similarity search
        similar_docs = self.perform_similarity_search(text_content)
        context_text = "\n".join([doc[0] for doc in similar_docs])
        
        # 5. Create prompt
        prompt = self.create_prompt(context_text, text_content)
        
        # 6. Call LLM API
        llm_response = self.call_llm_api(prompt)
        if not llm_response:
            return Response({"error": "Failed to get a response from LLM API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # 7. Parse response
        parsed_response = self.parse_llm_response(llm_response)
        
        # 8. Return response
        return Response(parsed_response, status=status.HTTP_200_OK)

    def extract_text_from_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            text = "".join(page.get_text() for page in doc)
            return text
        except Exception as e:
            logger.exception(f"Failed to extract text from PDF at {pdf_path}: {str(e)}")
            return ""

    def perform_similarity_search(self, query_text):
        try:
            embedding_function = OpenAIEmbeddings()
            db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
            results = db.similarity_search_with_relevance_scores(query_text, k=3)
            return results
        except Exception as e:
            logger.exception(f"Similarity search failed: {str(e)}")
            return []

    def create_prompt(self, context, question):
        return PROMPT_TEMPLATE.format(context=context, question=question)

    def call_llm_api(self, prompt):
        if not LLM_API_KEY:
            logger.error("LLM_API_KEY is not set in environment variables.")
            return ""

        model = ChatOpenAI(api_key=LLM_API_KEY)
        response = model.predict(prompt)
        return response

    def parse_llm_response(self, response_text):
        try:
            analysis_data = json.loads(response_text)
            lecture_goals = analysis_data.get('lecture_goals', 'No specific goals identified.')
            lecture_topics = analysis_data.get('lecture_topics', [])
            topic_tags = analysis_data.get('topic_tags', [])
            return {
                'lecture_goals': lecture_goals,
                'lecture_topics': lecture_topics,
                'topic_tags': topic_tags
            }
        except json.JSONDecodeError:
            logger.error(f"Failed to parse LLM response as JSON. Response: {response_text}")
            return {
                'lecture_goals': 'No specific goals identified.',
                'lecture_topics': [],
                'topic_tags': []
            }

class CodingLessonViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CodingLesson instances.
    """
    queryset = CodingLesson.objects.all().order_by('-created_at')
    serializer_class = CodingLessonSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def exercises(self, request, pk=None):
        """
        Retrieves all exercises related to a specific CodingLesson.
        """
        lesson = self.get_object()
        exercises = lesson.exercises.all()
        serializer = CodingExerciseSerializer(exercises, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """
        Retrieves all student interactions related to a specific CodingLesson.
        """
        lesson = self.get_object()
        interactions = lesson.interactions.all()
        serializer = StudentInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def common_questions(self, request, pk=None):
        """
        Retrieves all common questions related to a specific CodingLesson.
        """
        lesson = self.get_object()
        common_questions = lesson.common_questions_set.all()
        serializer = CommonQuestionSerializer(common_questions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def struggle_topics(self, request, pk=None):
        """
        Retrieves all struggle topics related to a specific CodingLesson.
        """
        lesson = self.get_object()
        struggle_topics = lesson.struggle_analyses.all()
        serializer = StruggleAnalysisSerializer(struggle_topics, many=True)
        return Response(serializer.data)

class CodingExerciseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CodingExercise instances.
    """
    queryset = CodingExercise.objects.all().order_by('-created_at')
    serializer_class = CodingExerciseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def interactions(self, request, pk=None):
        """
        Retrieves all student interactions related to a specific CodingExercise.
        """
        exercise = self.get_object()
        interactions = exercise.interactions.all()
        serializer = StudentInteractionSerializer(interactions, many=True)
        return Response(serializer.data)

class StudentInteractionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing StudentInteraction instances.
    """
    queryset = StudentInteraction.objects.all().order_by('-timestamp')
    serializer_class = StudentInteractionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override create method to handle student interactions.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        interaction = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CommonQuestionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing CommonQuestion instances.
    """
    queryset = CommonQuestion.objects.all().order_by('-frequency')
    serializer_class = CommonQuestionSerializer
    permission_classes = [IsAuthenticated]

class StruggleAnalysisViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing StruggleAnalysis instances.
    """
    queryset = StruggleAnalysis.objects.all().order_by('-frequency')
    serializer_class = StruggleAnalysisSerializer
    permission_classes = [IsAuthenticated]