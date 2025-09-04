README

Overview
--------
This project demonstrates dynamic Python code execution using the `exec` function.
It defines a function `B` that takes a Python code string, wraps it inside another
function, and executes it dynamically.

The example provided computes the 11th Fibonacci number using a recursive function.

Files
-----
- main.py – The script that runs the code.

Code Explanation
----------------

1. Importing Required Module
   ```python
   import textwrap
   ```
   The `textwrap` module is used to indent code so that it can be safely wrapped
   inside another function.

2. Function B(pys)
   ```python
   def B(pys):
       exec(pys, globals(), {})
   ```
   - Takes a Python code string (`pys`).
   - Executes it dynamically using Python’s built-in `exec`.
   - The code is executed in the global scope so that defined functions are accessible.

3. Example Python Code (Recursive Fibonacci)
   ```python
   pys = """
   def fibonacci(n):
       if n == 1 or n == 2:
           r = 1
       else:
           r = fibonacci(n - 1) + fibonacci(n - 2)
       return r

   print(fibonacci(11))
   """
   ```
   This block defines:
   - A recursive Fibonacci function.
   - Prints the 11th Fibonacci number (result = 89).

4. Wrapping the Code
   ```python
   def wrap(s):
       return "def foo():\n" "{}\n" "foo()".format(textwrap.indent(s, " " * 4))
   ```
   - Wraps the given code inside a function called `foo`.
   - Uses `textwrap.indent` to indent the code properly.
   - Calls `foo()` so the code executes when passed to `exec`.

   Example Output of `wrap(pys)`:
   ```python
   def foo():
       def fibonacci(n):
           if n == 1 or n == 2:
               r = 1
           else:
               r = fibonacci(n - 1) + fibonacci(n - 2)
           return r

       print(fibonacci(11))
   foo()
   ```

5. Executing the Wrapped Code
   ```python
   B(wrap(pys))
   ```
   - Calls `wrap(pys)` to prepare the code.
   - Passes the wrapped code to `B`, which executes it.
   - Prints:
   ```
   89
   ```

Output
------
When you run the script:
```
89
```

Key Concepts
------------
- Dynamic Execution: Running code strings using `exec`.
- Code Wrapping: Ensuring code is scoped inside a function to prevent accidental global pollution.
- Recursion: Fibonacci series implementation using recursive calls.

Example Modification
--------------------
You can replace `pys` with any custom Python function, and it will execute dynamically:
```python
pys = """
def greet(name):
    print("Hello,", name)

greet("testing")
"""
B(wrap(pys))
```

Output:
```
Hello, testing
```
