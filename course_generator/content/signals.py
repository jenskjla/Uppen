# # content/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import CodingLesson
# from .tasks import analyze_lecture_pdf  # Celery task to analyze lecture PDF

# @receiver(post_save, sender=CodingLesson)
# def trigger_lecture_analysis(sender, instance, created, **kwargs):
#     """
#     Signals Django to run analyze_lecture_pdf task whenever a new CodingLesson is created.
#     """
#     if created:
#         analyze_lecture_pdf.delay(instance.id)
