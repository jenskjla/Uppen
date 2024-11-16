import argparse
from langchain_openai import OpenAIEmbeddings
from langchain.evaluation import load_evaluator
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('word1', type=str, help='First word for embedding comparison')
    parser.add_argument('word2', type=str, help='Second word for embedding comparison')
    args = parser.parse_args()

    embedding_function = OpenAIEmbeddings()
    evaluator = load_evaluator("pairwise_embedding_distance")
    x = evaluator.evaluate_string_pairs(prediction=args.word1, prediction_b=args.word2)
    print(f"Comparing ({args.word1}, {args.word2}): {x}")

if __name__ == "__main__":
    main()
