import argparse
from dotenv import load_dotenv
import os
import requests
# from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
load_dotenv()

CHROMA_PATH = "chroma-data"
                                                                                                                                                                                                        
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = OpenAIEmbeddings()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=3)
    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    # model = ChatOpenAI()
    # response_text = model.predict(prompt)
    url = "https://proxy.tune.app/chat/completions"
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
        "model": "NLNHSR/NLNHSR-llama3-1-8b",
        "max_tokens": 300,
        "temperature": 0.5,
        "top_p": 0.9,
        "n": 1,
    }
    headers = {
        "X-Org-Id": "0266c7a8-a772-47c1-a450-b02275131dc7",
        "Authorization": "Bearer sk-tune-nBUsrB2PKHYgYu98pLUG3sTmIDpSkegHzis",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    response_text = response.text

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()