from math import ceil
import numpy as np
import matplotlib.pyplot as plt
import tabulate

from matplotlib import colors as mcolors
from IPython.display import HTML, display, Markdown


def rainbow_color(size):
    """Return a color list of size element lire rainbow
    """
    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                    for name, color in colors.items())
    by_hsv = by_hsv[2:]
    sorted_names = [name for hsv, name in by_hsv]
    modulo = ceil(len(sorted_names) / size)
    return sorted_names[::modulo]


def display_week_summary(day, psr, deviation):
    """Display summary of data of the week in iPython Notebook
    day : datetime.datetime.now()
    psr : pivot_sr(H, B, C)
    deviation : deviation(close=4797, volatility=23.13, period=5, precision=0)
    """
    week = day.isocalendar()[1]
    display(Markdown('''### Semaine {}
- 1 $\sigma$ [{} - {}]
- 2 $\sigma$ [{} - {}]
- Pivot {}
- SR1 [{} - {}]
- SR2 [{} - {}]
- SR3 [{} - {}]
    '''.format(week,
               round(deviation['1']['min']), round(deviation['1']['max']),
               round(deviation['2']['min']), round(deviation['2']['max']),
               round(psr['pivot']),
               round(psr['R1']), round(psr['S1']),
               round(psr['R2']), round(psr['S2']),
               round(psr['R3']), round(psr['S3'])
              )
    ))


class Graph:
    def __init__(self, min, max, step=1, sdeviation=None):
        self.min = min
        self.max = max
        self.step = step
        self.sT = np.arange(self.min,self.max, self.step)
        self.sdeviation = sdeviation

    def _setup_profit(self, figsize=None):
        plt.style.use('dark_background')
        if figsize:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig, ax = plt.subplots()
        ax.spines['top'].set_visible(False)  # Top border removed
        ax.spines['right'].set_visible(False)  # Right border removed
        ax.spines['bottom'].set_position('zero')  # Sets the X-axis in the center
        if self.sdeviation:
            plt.axvspan(self.sdeviation[0], self.sdeviation[1], facecolor='#2ca02c', alpha=0.5)
        return fig, ax

    def _show_profit(self, y, label, color):
        fig, ax = self._setup_profit()
        ax.plot(self.sT, y, label=label,color=color)
        plt.xlabel('Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend(loc='best')
        plt.show()

    def _show_profit_compare(self, y1, label1, color1, y2, label2, color2):
        fig, ax = self._setup_profit()
        ax.plot(self.sT, y1, label=label1,color=color1)
        ax.plot(self.sT, y2, label=label2,color=color2)
        ax.plot(self.sT, y2-y1, dashes=[10, 5, 10, 5], label='delta', color='orange')
        plt.xlabel('Stock Price')
        plt.ylabel('Profit and loss')
        plt.legend(loc='best')
        plt.show()

    def profit_from_payoff(self, payoff, label=None, color='r'):
        self._show_profit(payoff, label, color)

    def profit(self, option, direction, label=None, color='r'):
        payoff = option.payoff(self.sT, direction)
        label = str(option)
        self._show_profit(payoff, label, color)

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
        self._show_profit_compare(payoff_a, label_a, color_a,
                                  payoff_b, label_b, color_b
                                 )

    def profit_strategy(self, strategy, color='chartreuse'):
        payoff = strategy.payoff(self.sT)
        label = str(strategy)
        self._show_profit(payoff, label, color)

    def display_summary(self, strategy):
        detailst = [[l['cat'], l['strike'], l['direction'], l['quantity'], l['cost'], l['premium']]
                    for l in strategy.summary()]
        headers=['Category', 'strike', 'direction', 'Quantity', 'Cost', 'Premium']
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
        fig, ax = self._setup_profit(figsize=(12, 10))
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