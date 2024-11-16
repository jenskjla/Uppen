# content/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CodingLessonViewSet,
    CodingExerciseViewSet,
    StudentInteractionViewSet,
    CommonQuestionViewSet,
    StruggleAnalysisViewSet,
    LectureViewSet
)



router = DefaultRouter()
router.register(r'lessons', CodingLessonViewSet, basename='lesson')
router.register(r'exercises', CodingExerciseViewSet, basename='exercise')
router.register(r'interactions', StudentInteractionViewSet, basename='interaction')
router.register(r'common-questions', CommonQuestionViewSet, basename='commonquestion')
router.register(r'struggle-topics', StruggleAnalysisViewSet, basename='struggleanalysis')
router.register(r'lectures', LectureViewSet, basename='lecture')
# path('process-lecture/', ProcessLectureView.as_view(), name='process_lecture'),

urlpatterns = [
    path('', include(router.urls)),
]
