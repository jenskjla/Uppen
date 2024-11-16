// src/components/Content.js
import React from "react";
import './Content.css';

const Content = () => {
  return (
    <div className="content">
      <h2>Lesson Content</h2>
      <div>
        <h1>Recursion in OCaml</h1>
        <p>Recursion is a fundamental concept in functional programming where a function calls itself to solve a smaller instance of the same problem. In OCaml, recursion is used to iterate over data structures such as lists or to perform calculations such as factorials.</p>

        <h2>Key Concepts</h2>
        <ul>
          <li><strong>Recursive Function:</strong> A function that calls itself.</li>
          <li><strong>Base Case:</strong> A condition that stops the recursion, preventing an infinite loop.</li>
          <li><strong>Recursive Case:</strong> The part of the function that calls itself with a smaller or simpler argument.</li>
        </ul>

        <h2>Example: Factorial Function</h2>
        <pre><code>let rec factorial n = 
if n = 0 then 1 
else n * factorial (n - 1);;</code></pre>

        <h2>Explanation</h2>
        <ul>
          <li><strong>Base case:</strong> If <code>n = 0</code>, return 1.</li>
          <li><strong>Recursive case:</strong> Multiply <code>n</code> by the result of <code>factorial (n - 1)</code>.</li>
        </ul>

        <h2>Recursive List Processing</h2>
        <p>Recursion is often used to process lists in OCaml. For example, the function below sums all elements in a list:</p>
        <pre><code>let rec sum_list lst =
match lst with
| [] -&gt; 0
| x :: xs -&gt; x + sum_list xs;;</code></pre>

        <h2>Explanation</h2>
        <ul>
          <li><strong>Base case:</strong> If the list is empty (<code>[]</code>), return 0.</li>
          <li><strong>Recursive case:</strong> Take the first element <code>x</code> and add it to the sum of the rest of the list <code>sum_list xs</code>.</li>
        </ul>

        <h2>MCQ Quiz</h2>
        <div className="question">
          <p><strong>1. What is the base case in the following recursive function?</strong></p>
          <pre><code>let rec length lst =
match lst with
| [] -&gt; 0
| _ :: xs -&gt; 1 + length xs;;</code></pre>
          <ol>
            <li><input type="radio" name="q1" /> A. <code>1 + length xs</code></li>
            <li><input type="radio" name="q1" /> B. <code>match lst with</code></li>
            <li><input type="radio" name="q1" /> C. <code>[] -&gt; 0</code></li>
            <li><input type="radio" name="q1" /> D. <code>_ :: xs</code></li>
          </ol>
        </div>

        <div className="question">
          <p><strong>2. What happens if a recursive function does not have a base case?</strong></p>
          <ol>
            <li><input type="radio" name="q2" /> A. The function will compile successfully.</li>
            <li><input type="radio" name="q2" /> B. The function will run indefinitely and may cause a stack overflow.</li>
            <li><input type="radio" name="q2" /> C. The function will throw an error before execution.</li>
            <li><input type="radio" name="q2" /> D. The function will return <code>None</code>.</li>
          </ol>
        </div>

        <h2>Fill in the Blanks</h2>
        <div className="question">
          <p><strong>1. In a recursive function, the __________ is the condition that terminates the recursion.</strong></p>
          <input type="text" size="30" />
        </div>

        <div className="question">
          <p><strong>2. A recursive function calls __________ to solve smaller instances of the same problem.</strong></p>
          <input type="text" size="30" />
        </div>

        <h2>Short Answer</h2>
        <div className="question">
          <p><strong>1. Write a recursive function in OCaml that returns the maximum value in a list.</strong></p>
          <textarea rows="5" cols="50"></textarea>
        </div>

        <div className="question">
          <p><strong>2. What is tail recursion and why is it important in OCaml?</strong></p>
          <textarea rows="5" cols="50"></textarea>
        </div>

        <h2>Recursion vs Iteration</h2>
        <p>While recursion and iteration can often achieve the same results, recursion is more common in functional programming. However, recursion in OCaml must be carefully managed to avoid excessive memory usage or stack overflows. <strong>Tail recursion</strong> is a form of recursion where the recursive call is the last operation in the function. Tail-recursive functions are optimized by the compiler to reuse the current function's stack frame, which avoids stack overflows and improves efficiency.</p>

        <h3>Example: Tail-Recursive Sum Function</h3>
        <pre><code>let rec sum_list_tail lst acc =
match lst with
| [] -&gt; acc
| x :: xs -&gt; sum_list_tail xs (acc + x);;</code></pre>

        <h2>Conclusion</h2>
        <p>Recursion is a powerful tool in OCaml, particularly for list processing and mathematical computations. Understanding how to structure recursive functions with a proper base case and recursion step is crucial for functional programming in OCaml. Tail recursion is particularly important for writing efficient recursive functions.</p>
      </div>
    </div>
  );
};

export default Content;
