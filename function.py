from jinja2 import Template
import matplotlib.pyplot as plt


def create_plot(x: list[float], y: list[float], plot_name: str) -> str:
    line = plt.plot(x, y)
    plt.setp(line, color="blue", linewidth=2)
    plt.gca().spines["left"].set_position("zero")
    plt.gca().spines["bottom"].set_position("zero")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig(plot_name)
    return plot_name


def f(x: float) -> float:
    return x ** 3 - 6 * x ** 2 + x + 5


a = -2
b = 6
n = 30
h = (b - a) / (n - 1)

x_list = [a + i * h for i in range(n)]
f_list = [f(x) for x in x_list]

if __name__ == '__main__':
    with open('function_template.jinja2', 'r', encoding='utf-8-sig') as infile:
        html = infile.read()

    template = Template(html)
    template.globals["len"] = len
    template.globals["round"] = round

    with open('function.html', 'w', encoding='utf-8-sig') as outfile:
        result_html = template.render(x=x_list, y=f_list, plot=create_plot(x_list, f_list, "function.jpg"))
        outfile.write(result_html)
