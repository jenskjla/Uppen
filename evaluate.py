import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ChatGPT-based evaluation function (replaced with Tune API)
def evaluate_lesson_tune(lesson):
    # Prompt for evaluation
    prompt = f"""
    Please evaluate the following lesson plan based on three criteria: depth, engagement, and diversity of topics/problems. 
    Provide a score from 0 to 5 for each criterion and a short reasoning for each score. 
    
    Lesson Plan:
    {lesson}

    Criteria:
    1. Depth: Does the lesson provide detailed explanations and cover advanced aspects of the topic?
    2. Engagement: Does the lesson offer a variety of interactive elements such as questions, challenges, and exercises?
    3. Diversity: Does the lesson cover different aspects of the topic (e.g., varied examples, problems, or applications)?
    
    Provide the score as a JSON object with the keys "depth", "engagement", and "diversity" and explain the reasoning for each score. Do not provide anything except the JSON object.
    """

    # Tune API call
    url = "https://proxy.tune.app/chat/completions"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "NLNHSR/NLNHSR-llama3-1-8b",
        "max_tokens": 300,
        "temperature": 0.5,
        "top_p": 0.9,
        "n": 1,
    }
    headers = {
        "X-Org-Id": os.getenv("ORGANIZATION_ID"),
        "Authorization": os.getenv("AUTHORIZATION_ID"),
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = response.json()
    
    # Extract the response (assuming the result contains a JSON-like structure)
    scores = eval(result['choices'][0]['message']['content'].strip())

    return scores

# Function to filter lessons based on Tune API scores
def filter_lessons_tune(lessons, depth_threshold=3, engagement_threshold=3, diversity_threshold=3):
    top_lessons = []
    
    for lesson in lessons:
        # Get scores from Tune API
        scores = evaluate_lesson_tune(lesson)
        
        # Check if lesson meets all threshold criteria
        if (scores["depth"] >= depth_threshold and
            scores["engagement"] >= engagement_threshold and
            scores["diversity"] >= diversity_threshold):
            top_lessons.append({
                "lesson": lesson,
                "scores": scores
            })
    
    return top_lessons

# Function to merge the best parts of the top lessons using Tune API
def merge_best_parts_tune(top_lessons, max_length=500):
    # Combine the good lessons for Tune API to process
    merged_lesson = "\n".join([lesson["lesson"] for lesson in top_lessons])
    
    # Create a prompt to merge the best parts into one cohesive lesson plan
    prompt = f"""
    You are provided with several good lesson plans below. Your task is to extract the best parts (explanations, examples, and problems) 
    from these lessons and combine them into a single cohesive lesson plan without increasing the total length beyond {max_length} tokens. 
    Ensure the final lesson has sufficient depth, engagement, and diversity, and that it provides varied examples and problems.
    
    Lessons:
    {merged_lesson}

    Final merged lesson plan should include:
    1. The best explanation from the lessons.
    2. The most diverse and engaging examples.
    3. A variety of practice problems or exercises.
    
    Output the final merged lesson plan without exceeding {max_length} tokens.
    """

    url = "https://proxy.tune.app/chat/completions"
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "NLNHSR/NLNHSR-llama3-1-8b",
        "max_tokens": max_length,
        "temperature": 0.5,
        "top_p": 0.9,
        "n": 1,
    }
    headers = {
        "X-Org-Id": "ORGANIZATION_ID",
        "Authorization": "AUTHORIZATION_ID",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    result = response.json()

    # Extract the merged lesson from the response
    merged_lesson_plan = result['choices'][0]['message']['content'].strip()
    
    return merged_lesson_plan

# Example usage: sample lessons (you would replace this with actual lesson content)
lesson_1 = """
Lesson on Python functions: covers basic syntax, parameters, and return values. It includes two exercises on defining and using functions.
"""
lesson_2 = """
Lesson on Recursion in Functional Programming: covers recursion fundamentals, factorial function, and a simple problem-solving exercise.
"""
lesson_3 = """
Lesson on Algorithms: covers sorting algorithms, including bubble sort and quicksort, with multiple examples and a code challenge.
"""

lessons = [lesson_1, lesson_2, lesson_3]

# Step 1: Evaluate and filter lessons
top_lessons = filter_lessons_tune(lessons)

if top_lessons:
    # Step 2: Merge the best parts from the top lessons
    final_merged_lesson_plan = merge_best_parts_tune(top_lessons, max_length=500)

    print("Final Merged Lesson Plan:")
    print(final_merged_lesson_plan)
else:
    print("No lessons met the threshold criteria.")
