import numpy as np
import matplotlib.pyplot as plt


def show_profit(x, y, label, color):    
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False) # Top border removed
    ax.spines['right'].set_visible(False) # Right border removed
    ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
    ax.plot(x, y, label=label,color=color)
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and loss')
    plt.legend()
    # plt.title('Profit Scheme')
    plt.show()
def show_profit_compare(x, y1, label1, color1, y2, label2, color2):    
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False) # Top border removed
    ax.spines['right'].set_visible(False) # Right border removed
    ax.spines['bottom'].set_position('zero') # Sets the X-axis in the center
    ax.plot(x, y1, label=label1,color=color1)
    ax.plot(x, y2, label=label2,color=color2)
    ax.plot(x, y2-y1, dashes=[10, 5, 10, 5], label='delta', color='g')
    plt.xlabel('Stock Price')
    plt.ylabel('Profit and loss')
    plt.legend()
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
                label_b=None, color_b='b'):
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
    def profit_strategy(self, strategy, color='b'):
        payoff = strategy.payoff(self.sT)
        label = str(strategy)
        show_profit(self.sT, payoff, label, color)
