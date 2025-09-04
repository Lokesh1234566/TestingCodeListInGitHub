import textwrap


def B(pys):
    exec(pys, globals(), {})


pys = """
def fibonacci(n):
    if n == 1 or n == 2:
        r = 1
    else:
        r = fibonacci(n - 1) + fibonacci(n - 2)
    return r

print(fibonacci(11))
"""


def wrap(s):
    return "def foo():\n" "{}\n" "foo()".format(textwrap.indent(s, " " * 4))


B(wrap(pys))
