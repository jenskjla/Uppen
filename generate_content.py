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

CHROMA_PATH = "chroma"
                                                                                                                                                                                                        
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    content = """
    I want to learn about recursion in ocaml
    ChatGPT said:
    ChatGPT
    Recursion in OCaml is one of the fundamental concepts and is used extensively due to the language's functional nature. Here’s an introduction to recursion in OCaml:

    What is Recursion?
    Recursion is a programming technique where a function calls itself to solve smaller instances of the same problem. Recursive functions often have two main components:

    Base Case: The condition that stops the recursion.
    Recursive Case: The part where the function calls itself with a modified argument.
    Writing Recursive Functions in OCaml
    In OCaml, to define a recursive function, you need to use the rec keyword. Here's the general syntax:

    ocaml
    Copy code
    let rec function_name argument = 
        if base_case then
            base_case_result
        else
            recursive_case
    Example 1: Factorial Function
    Let’s start with a simple example, the factorial function (n!), which is defined as: 𝑛!=𝑛×(𝑛−1)×(𝑛−2)×⋯×1
    This can be written recursively as:

    Base Case: 
    0!=1
    Recursive Case: 
    n!=n×(n−1)!
    Here's how you can implement it in OCaml:

    ocaml
    Copy code
    let rec factorial n =
        if n = 0 then 1  (* Base case *)
        else n * factorial (n - 1)  (* Recursive call *)
    Example 2: Fibonacci Sequence
    Another classic example of recursion is the Fibonacci sequence. The nth Fibonacci number is defined as:
    F(n)=F(n−1)+F(n−2)
    With base cases:
    F(0)=0
    F(1)=1
    Here’s how to write the Fibonacci function in OCaml:

    ocaml
    Copy code
    let rec fibonacci n =
        if n = 0 then 0
        else if n = 1 then 1
        else fibonacci (n - 1) + fibonacci (n - 2)
    Example 3: Sum of a List
    You can also use recursion to perform operations on lists. For example, finding the sum of all elements in a list:

    Base Case: The sum of an empty list is 0.
    Recursive Case: The sum of a list is the first element plus the sum of the rest of the list.
    ocaml
    Copy code
    let rec sum_list lst = 
        match lst with
        | [] -> 0  (* Base case: Empty list *)
        | head :: tail -> head + sum_list tail  (* Recursive case *)
    Key Points to Keep in Mind:
    Tail Recursion: Tail recursion is a special form of recursion where the recursive call is the last thing executed in the function. It’s important in OCaml because it allows the compiler to optimize the recursion and avoid stack overflow errors for large inputs. Tail-recursive functions are more memory-efficient.

    Tail-Recursive Example: Factorial

    Here’s a tail-recursive version of the factorial function:

    ocaml
    Copy code
    let rec factorial_tailrec n acc =
        if n = 0 then acc
        else factorial_tailrec (n - 1) (n * acc)
        
    let factorial n = factorial_tailrec n 1
    In this version, the function passes an additional accumulator acc to store the result of the computation. This allows the recursion to be optimized.

    Example 4: Reversing a List (Tail Recursion)
    Another example using tail recursion is reversing a list:

    ocaml
    Copy code
    let rec reverse_tailrec lst acc =
        match lst with
        | [] -> acc
        | head :: tail -> reverse_tailrec tail (head :: acc)
        
    let reverse lst = reverse_tailrec lst []
    Here, we maintain an accumulator acc that holds the reversed portion of the list.

    Would you like to dive deeper into tail recursion or explore other examples?


    2/2

    You said:
    When it specifically asks for forward recursion, what can I do?
    ChatGPT said:
    ChatGPT
    Forward recursion generally refers to a form of recursion where the recursive function builds up from the "beginning" or base case, typically moving forward through a structure like a list, and constructs a result as it progresses through each recursive step.

    Forward Recursion Example: List Summation
    In the list summation example I shared earlier, we’re essentially using forward recursion:

    ocaml
    Copy code
    let rec sum_list lst = 
        match lst with
        | [] -> 0  (* Base case: empty list *)
        | head :: tail -> head + sum_list tail  (* Recursive step *)
    Here, the function starts with the base case (empty list) and moves forward by summing each head element of the list and combining it with the result of the recursive call on the rest of the list.

    This approach is forward recursion because each recursive step processes the head of the list and combines it with the result from the rest of the list (tail), effectively "moving forward" through the list.

    Example: Building a List (Forward Recursion)
    Another example of forward recursion is constructing a list. Imagine we want to create a list from 1 to n:

    ocaml
    Copy code
    let rec build_list n =
        if n = 0 then []  (* Base case: empty list *)
        else build_list (n - 1) @ [n]  (* Recursive step: append n to the result of build_list (n-1) *)
    This example recursively calls build_list (n-1) and appends the current value n at each step. Note that @ is the list concatenation operator in OCaml. The result builds up by appending each element to the list produced by the recursive call.

    Example: Forward Recursion in Tree Traversal
    For data structures like trees, forward recursion can also be applied. Here’s an example of forward recursion that performs a pre-order traversal of a binary tree (visiting the current node first, then the left subtree, and finally the right subtree):

    ocaml
    Copy code
    type 'a tree = Empty | Node of 'a * 'a tree * 'a tree

    let rec preorder tree =
        match tree with
        | Empty -> []
        | Node(value, left, right) ->
            [value] @ preorder left @ preorder right
    In this example, we first visit the current node ([value]), then traverse the left subtree (preorder left), and finally the right subtree (preorder right). The recursive process builds up the final list in a forward manner.

    Forward Recursion with List Mapping
    Another common scenario for forward recursion is applying a function to each element of a list, such as mapping a function over a list:

    ocaml
    Copy code
    let rec map f lst =
        match lst with
        | [] -> []  (* Base case: empty list *)
        | head :: tail -> (f head) :: (map f tail)  (* Apply f to head and recurse *)
    Here, the function map recursively applies the function f to each element of the list, building up the result list by combining the result of f head with the result of recursively applying map to the rest of the list.

    Key Considerations for Forward Recursion:
    Order Matters: Forward recursion builds up a result starting from the base case, typically processing each element in a structure (e.g., list, tree) in order and constructing the result step-by-step.
    Efficiency: Forward recursion can sometimes be less efficient due to operations like list concatenation (@), which can be costly if not optimized.
    In summary, for forward recursion, focus on:

    Starting from a base case (like an empty list or zero).
    Recursively moving through the structure (list, tree, etc.) while building up the result in each step.
    Would you like to see how to optimize forward recursion using techniques like tail recursion, or have other questions on recursion?

    """
    query_text = f"""
    Using past student's learning experience: {content},
    Generate an educational content containing the following information:
    introduction to the topic, key concepts, examples and their explanation, Multiple Choice Questions (MCQs), Fill in the Blank Questions, and short answer questions.
    Provide the content in HTML format. Do not provide anything except the HTML.
    """

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
        "max_tokens": 2000,
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

    response_text = response.text

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()