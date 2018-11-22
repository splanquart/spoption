from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import tabulate

from matplotlib import colors as mcolors
from IPython.display import HTML, display


def rainbow_color(size):
    """Return a color list of size element lire rainbow
    """
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                    for name, color in colors.items())
    sorted_names = [name for hsv, name in by_hsv]
    modulo = ceil(len(sorted_names) / size)
    return sorted_names[::modulo]

def show_profit(x, y, label, color):    
    fig, ax = plt.subplots()
    plt.style.use('dark_background')
    ax.spines['top'].set_visible(False)  # Top border removed
    ax.spines['right'].set_visible(False)  # Right border removed
    ax.spines['bottom'].set_position('zero')  # Sets the X-axis in the center
    ax.plot(x, y, label=label,color=color)
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and loss')
    plt.legend(loc='best')
    # plt.title('Profit Scheme')
    plt.show()
def show_profit_compare(x, y1, label1, color1, y2, label2, color2):    
    fig, ax = plt.subplots()
    plt.style.use('dark_background')
    ax.spines['top'].set_visible(False)  # Top border removed
    ax.spines['right'].set_visible(False)  # Right border removed
    ax.spines['bottom'].set_position('zero')  # Sets the X-axis in the center
    ax.plot(x, y1, label=label1,color=color1)
    ax.plot(x, y2, label=label2,color=color2)
    ax.plot(x, y2-y1, dashes=[10, 5, 10, 5], label='delta', color='g')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and loss')
    plt.legend(loc='best')
    plt.show()

class Graph:
    def __init__(self, min, max, step=1):
        self.min = min
        self.max = max
        self.step = step
        self.sT = np.arange(self.min,self.max,self.step)
    def profit_from_payoff(self, payoff, label=None, color='r'):
        show_profit(self.sT, payoff, label, color)
    def profit(self, option, direction, label=None, color='r'):
        payoff = option.payoff(self.sT, direction)
        label = str(option)
        show_profit(self.sT, payoff, label, color)
    def compare(self,
                option_a, direction_a, option_b, direction_b,
                label_a=None, color_a='r',
                label_b=None, color_b='chartreuse'):
        if not label_a:
            label_a = '{} {}'.format(str(option_a), direction_a)
        if not label_b:
            label_b = '{} {}'.format(str(option_b), direction_b)
        payoff_a = option_a.payoff(self.sT, direction_a)
        payoff_b = option_b.payoff(self.sT, direction_b)
        show_profit_compare(self.sT,
                            payoff_a, label_a, color_a,
                            payoff_b, label_b, color_b
                           )
    def profit_strategy(self, strategy, color='chartreuse'):
        payoff = strategy.payoff(self.sT)
        label = str(strategy)
        show_profit(self.sT, payoff, label, color)
    def display_summary(self, strategy):
        detailst = [[l['cat'], l['strike'], l['direction'], l['quantity'], l['cost']]
                    for l in strategy.summary()]
        headers=['Category', 'strike', 'direction', 'Quantity', 'Cost']
        display(HTML(tabulate.tabulate(detailst, tablefmt='html', headers=headers)))
    def display_page_raw(self, page):
        headers=['Settl.C', 'OIC', 'Day Vol C', 'Last C', 'bid C', 'ask C','C',
                 'strike', 'P', 'bid P', 'ask P', 'Last P', 'Day Vol P', 'OIP', 'Settl.P']
        display(HTML(tabulate.tabulate(page.data, tablefmt='html', headers=headers)))
    def profit_rainbow(self, assets, direction, title=None):
        """
        :param assets: list of options or strategies to graph
        :param direction: str 'long' or 'short'

        >>> g.profit_rainbow(put.values,'short')
        """
        assets_color = [(key, value)
                      for key, value
                      in zip(assets, rainbow_color(len(assets)))]
        fig, ax = plt.subplots(figsize=(12, 10))
        plt.style.use('dark_background')
        ax.spines['top'].set_visible(False)  # Top border removed
        ax.spines['right'].set_visible(False)  # Right border removed
        ax.spines['bottom'].set_position('zero')  # Sets the X-axis in the center
        for idx, (asset, color) in enumerate(assets_color):
            y = asset.payoff(self.sT, direction)
            label = '#{:02} {}'.format(idx, asset.label)
            ax.plot(self.sT, y, label=label,color=color)
        plt.xlabel('Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend(loc='best')
        if title:
            plt.title(title)
        plt.show()