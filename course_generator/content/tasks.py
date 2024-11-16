# content/tasks.py

from celery import shared_task
from django.conf import settings
from .models import CodingLesson
import os
import logging
import json
import requests
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings

# Configure logger
logger = logging.getLogger(__name__)

# Constants (Adjust these as needed)
CHROMA_PATH = os.path.join(settings.BASE_DIR, 'chroma')  # Path to Chroma DB
PROMPT_TEMPLATE = """
Analyze the following lecture notes and extract the goals, topics covered, and relevant tags. Provide the information in a valid JSON format with the following keys: "lecture_goals", "lecture_topics", and "topic_tags".

Context:
{context}

Lecture Notes:
{question}
"""

LLM_API_URL = "https://proxy.tune.app/chat/completions"
LLM_MODEL = "openai/gpt-4o-mini"
LLM_MAX_TOKENS = 500
LLM_TEMPERATURE = 0.5
LLM_TOP_P = 0.9
LLM_N = 1
LLM_PRESENCE_PENALTY = 0.5
LLM_FREQUENCY_PENALTY = 0.3

# Securely retrieve API key from environment variables
LLM_API_KEY = os.getenv('TUNE_STUDIO_API_KEY')  # Ensure this is set in your environment


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using PyMuPDF.

    Args:
        pdf_path (str): The file path to the PDF.

    Returns:
        str: Extracted text content from the PDF.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        logger.exception(f"Failed to extract text from PDF at {pdf_path}: {str(e)}")
        return ""


def perform_similarity_search(query_text):
    """
    Performs a similarity search on the Chroma DB using the provided query text.

    Args:
        query_text (str): The text to query the Chroma DB.

    Returns:
        list: A list of tuples containing documents and their relevance scores.
    """
    try:
        embedding_function = OpenAIEmbeddings()
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        results = db.similarity_search_with_relevance_scores(query_text, k=3)
        return results
    except Exception as e:
        logger.exception(f"Similarity search failed: {str(e)}")
        return []


def create_prompt(context, question):
    """
    Creates a prompt for the LLM using the provided context and question.

    Args:
        context (str): The contextual text retrieved from similarity search.
        question (str): The question or instruction for the LLM.

    Returns:
        str: The formatted prompt.
    """
    return PROMPT_TEMPLATE.format(context=context, question=question)


def call_llm_api(prompt):
    """
    Calls the LLM API with the given prompt and retrieves the response.

    Args:
        prompt (str): The prompt to send to the LLM.

    Returns:
        str: The response text from the LLM.
    """
    if not LLM_API_KEY:
        logger.error("LLM_API_KEY is not set in environment variables.")
        return ""

    headers = {
        "X-Org-Id": "0266c7a8-a772-47c1-a450-b02275131dc7",
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an academic tutor for a programming languages and compilers college course."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": LLM_MODEL,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
        "top_p": LLM_TOP_P,
        "n": LLM_N,
        "presence_penalty": LLM_PRESENCE_PENALTY,
        "frequency_penalty": LLM_FREQUENCY_PENALTY,
    }

    try:
        response = requests.post(LLM_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        response_text = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
        return response_text
    except requests.exceptions.RequestException as e:
        logger.exception(f"LLM API request failed: {str(e)}")
        return ""


def parse_llm_response(response_text):
    """
    Parses the LLM response to extract lecture goals, topics, and tags.

    Args:
        response_text (str): The raw response text from the LLM.

    Returns:
        dict: A dictionary containing 'lecture_goals', 'lecture_topics', and 'topic_tags'.
    """
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


# @shared_task(bind=True, max_retries=3)
# def analyze_lecture_pdf(self, lesson_id):
#     """
#     Celery task to analyze a lecture PDF associated with a CodingLesson.
#     Extracts lecture goals, topics, and tags using an LLM and updates the CodingLesson instance.

#     Args:
#         lesson_id (int): The ID of the CodingLesson to analyze.
#     """
#     try:
#         # Retrieve the CodingLesson instance
#         lesson = CodingLesson.objects.get(id=lesson_id)
#         pdf_source = lesson.chroma_document_id  # Assuming this is the relative path to the PDF
#         pdf_filename = os.path.basename(pdf_source)
#         pdf_path = os.path.join(settings.BASE_DIR, 'data', pdf_filename)  # Adjust 'data' directory as needed

#         # Check if the PDF file exists
#         if not os.path.exists(pdf_path):
#             logger.error(f"PDF not found at path: {pdf_path} for lesson: {lesson.title}")
#             return

#         # Step 1: Extract text from PDF
#         extracted_text = extract_text_from_pdf(pdf_path)
#         if not extracted_text:
#             logger.error(f"No text extracted from PDF at {pdf_path} for lesson: {lesson.title}")
#             return

#         # Step 2: Perform similarity search
#         query_text = "Lecture Analysis"
#         results = perform_similarity_search(query_text)
#         if len(results) == 0 or results[0][1] < 0.7:
#             logger.warning(f"Unable to find matching results for similarity search in lesson: {lesson.title}")
#             return

#         # Step 3: Combine context from top results
#         context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])

#         # Step 4: Create prompt for LLM
#         prompt = create_prompt(context=context_text, question=query_text)

#         # Step 5: Call LLM API
#         response_text = call_llm_api(prompt)
#         if not response_text:
#             logger.error(f"No response received from LLM for lesson: {lesson.title}")
#             return

#         # Step 6: Parse LLM response
#         analysis = parse_llm_response(response_text)
#         if not analysis:
#             logger.error(f"Analysis data is empty for lesson: {lesson.title}")
#             return

#         # Step 7: Update CodingLesson instance
#         lesson.lecture_goals = analysis['lecture_goals']
#         lesson.lecture_topics = analysis['lecture_topics']
#         lesson.topic_tags = analysis['topic_tags']
#         lesson.save()

#         logger.info(f"Successfully analyzed and updated lesson: {lesson.title}")

#     except CodingLesson.DoesNotExist:
#         logger.error(f"CodingLesson with id {lesson_id} does not exist.")
#     except Exception as e:
#         # Retry the task in case of unexpected errors
#         try:
#             logger.exception(f"Error processing lecture PDF for lesson id {lesson_id}: {str(e)}. Retrying...")
#             self.retry(exc=e, countdown=60)  # Retry after 60 seconds
#         except self.MaxRetriesExceededError:
#             logger.error(f"Max retries exceeded for lesson id {lesson_id}. Task failed.")
