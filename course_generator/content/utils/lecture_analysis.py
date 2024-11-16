import requests
import os
import logging
import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from celery import shared_task
from models import CodingLesson
# from .utils.lecture_analysis import analyze_lecture_pdf_using_llm, parse_analysis_data
import os
import logging
# Initialize logger
logger = logging.getLogger(__name__)

CHROMA_PATH = "chroma"  # Ensure this matches your setup
PROMPT_TEMPLATE = "Analyze the following lecture notes and extract the goals, topics covered, and relevant tags.\n\n{context}\n\nLecture Notes:\n{question}"

# Initialize Chroma DB
embedding_function = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

def analyze_lecture_pdf_using_llm(pdf_path, query_text):
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if not results or results[0][1] < 0.7:
        logger.warning("No matching results found in Chroma DB.")
        return None

    # Combine context from top results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)

    # Prepare the API request
    url = "https://proxy.tune.app/chat/completions"
    payload = {
        "messages": [
            {"role": "system", "content": "You are an academic tutor for a programming languages and compilers college course."},
            {"role": "user", "content": prompt}
        ],
        "model": "openai/gpt-4o-mini",
        "max_tokens": 500,
        "temperature": 0.5,
        "top_p": 0.9,
        "n": 1,
        "presence_penalty": 0.5,
        "frequency_penalty": 0.3,
    }
    headers = {
        "X-Org-Id": os.environ.get("TUNE_STUDIO_ORG_ID"),
        "Authorization": f"Bearer {os.environ.get('TUNE_STUDIO_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        logger.error(f"API Error: {response.status_code} - {response.text}")
        return None

    response_data = response.json()
    response_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
    return response_text

def parse_analysis_data(analysis_text):
    try:
        analysis_data = json.loads(analysis_text)
        lecture_goals = analysis_data.get('lecture_goals', 'No specific goals identified.')
        lecture_topics = analysis_data.get('lecture_topics', [])
        topic_tags = analysis_data.get('topic_tags', [])
        return lecture_goals, lecture_topics, topic_tags
    except json.JSONDecodeError:
        logger.error(f"Failed to parse analysis data. Response: {analysis_text}")
        return None, None, None


logger = logging.getLogger(__name__)

@shared_task
def analyze_lecture_pdf(lesson_id):
    try:
        lesson = CodingLesson.objects.get(id=lesson_id)
        pdf_path = os.path.join('data', os.path.basename(lesson.chroma_document_id))
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF not found at path: {pdf_path} for lesson: {lesson.title}")
            return

        query_text = "Lecture Analysis"
        analysis_text = analyze_lecture_pdf_using_llm(pdf_path, query_text)

        if analysis_text:
            lecture_goals, lecture_topics, topic_tags = parse_analysis_data(analysis_text)
            if lecture_goals and lecture_topics and topic_tags:
                lesson.lecture_goals = lecture_goals
                lesson.lecture_topics = lecture_topics
                lesson.topic_tags = topic_tags
                lesson.save()
                logger.info(f"Successfully analyzed and updated lesson: {lesson.title}")
        else:
            logger.error(f"No analysis data received for lesson: {lesson.title}")

    except CodingLesson.DoesNotExist:
        logger.error(f"CodingLesson with id {lesson_id} does not exist.")
    except Exception as e:
        logger.exception(f"Error processing lecture PDF for lesson id {lesson_id}: {str(e)}")
