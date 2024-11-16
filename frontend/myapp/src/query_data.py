import argparse
from dotenv import load_dotenv
import os
import requests
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate

# Load environment variables from the .env file
load_dotenv()

# Constants
CHROMA_PATH = "chroma"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
TUNE_API_URL = "https://proxy.tune.app/chat/completions"
TUNE_API_ORG_ID = "0266c7a8-a772-47c1-a450-b02275131dc7"
TUNE_API_KEY = "Bearer sk-tune-nBUsrB2PKHYgYu98pLUG3sTmIDpSkegHzis"
MAX_TOKENS = 123
TEMPERATURE = 1.0
TOP_P = 1.0

def query_database(query_text):
    """
    Function to query the Chroma database using embeddings and return the result.
    """
    # Prepare the embedding function
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB for relevance
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        return None, None

    # Prepare context from the top results
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    return context_text, [doc.metadata.get("source", None) for doc, _score in results]

def create_prompt(context, question):
    """
    Function to create a prompt using the context and question.
    """
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context, question=question)
    return prompt

def call_tune_api(prompt):
    """
    Function to send the prompt to the Tune AI API and return the response.
    """
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an academic tutor for a programming languages and compilers college course"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "NLNHSR-llama3-1-8b",
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "top_p": TOP_P,
        "n": 1
    }

    headers = {
        "X-Org-Id": TUNE_API_ORG_ID,
        "Authorization": TUNE_API_KEY,
        "Content-Type": "application/json"
    }

    # Make the request to Tune AI API
    response = requests.post(TUNE_API_URL, json=payload, headers=headers)
    return response.text

def main():
    """
    Main function to handle query, fetch embeddings, and interact with the Tune AI API.
    """
    # Argument parser for CLI inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Query the Chroma database for relevant context
    context_text, sources = query_database(query_text)

    if not context_text:
        print("Unable to find matching results.")
        return

    # Create the prompt using the context and query
    prompt = create_prompt(context=context_text, question=query_text)

    # Call the Tune AI API with the generated prompt
    response_text = call_tune_api(prompt)

    # Format and print the response with sources
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()
