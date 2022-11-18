import math

from jinja2 import Template
import sympy as sp
import re

from function import create_plot


class FunctionData:
    def __init__(self, x: float, f: ()):
        self.x = x
        self.y = f(x)


class Function:
    def __init__(self, name: str, f: (), a: float, b: float, n: int):
        self.name = name
        self.f = f
        self.a = a
        self.b = b
        self.n = n
        self.data: list[FunctionData] = []

    @property
    def x(self) -> list[float]:
        return [data.x for data in self.data]

    @property
    def y(self) -> list[float]:
        return [data.y for data in self.data]

    def calculate(self) -> None:
        h = (self.b - self.a) / (self.n - 1)
        self.data = [FunctionData(x=self.a + i * h, f=self.f) for i in range(self.n)]

    def __str__(self):
        x = sp.Symbol("x", real=True)
        expression = sp.printing.latex(self.f(x))
        # Удаляет пробел между числом и x ("5 x" -> "5x")
        expression = re.sub(r"(\d) (x)", lambda m: f"{m[1]}{m[2]}", expression)
        # Меняет latex-степень на html-степень ("x^{2}" -> "x<sup>2</sup>")
        expression = re.sub(r"\^\{(\d+)}", lambda m: f"<sup>{m[1]}</sup>", expression)
        # Меняет latex-дробь на обычную дробь ("\frac{x + 1}{x - 2}" -> "(x + 1) / (x + 2)")
        expression = re.sub(
            r"\\frac\{(.+)}\{(.+)}", lambda m: f"{m[1] if m[1].find(' ') < 0 else f'({m[1]})'} / ({m[2]})",
            expression
        )
        return f"{self.name} = {expression}"


params = dict(a=-2, b=6, n=30)
functions = [
    Function("f(x)", lambda x: x ** 3 - 6 * x ** 2 + x + 5, **params),
    Function("y(x)", lambda x: x ** 2 - 5 * x + 1, **params),
    Function("z(x)", lambda x: 1 / (x ** 2 + 1), **params)
]
function1 = functions[0]
function2 = functions[2]
function3 = functions[1]
function = functions[1]
function1.calculate()
function2.calculate()
function3.calculate()

if __name__ == '__main__':
    with open('functions_template.jinja2', 'r', encoding='utf-8-sig') as infile:
        html = infile.read()

    template = Template(html)
    template.globals["round"] = round
    template.globals["len"] = len
    template.globals["floor"] = math.floor
    template.globals["ceil"] = math.ceil

    with open('functions.html', 'w', encoding='utf-8-sig') as outfile:
        result_html = template.render(
            functions=functions,
            function=function,
            max_lines=10,
            function1=function1,
            function2=function2,
            function3=function3,
            plot1=create_plot(x=function1.x, y=function1.y, plot_name="functions1.jpg"),
            plot2=create_plot(x=function2.x, y=function2.y, plot_name="functions2.jpg"),
            plot3=create_plot(x=function3.x, y=function3.y, plot_name="functions3.jpg"),
        )
        outfile.write(result_html)
