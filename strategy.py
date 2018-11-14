import numpy as np
from math import ceil, floor


class Strategy:
    def __init__(self, label=''):
        self.label = label
        self.options = []
    def add(self, option, direction, quantity):
        self.options.append({'option': option,
                             'direction': direction,
                             'quantity':quantity})
        return self
    def payoff(self, sT, direction='long'):
        payoff_sum = 0
        for o in self.options:
            option = o['option']
            direct = o['direction']
            quantity = o['quantity']
            payoff = option.payoff(sT, direct) * quantity
            payoff_sum += payoff
        return payoff_sum
    def __str__(self):
        return self.label if self.label else 'Strategy'
    def summary(self):
        """return summary of strategy to apply it:
        category, strike, direction, quantity and cost
        """
        return [{'cat': o['option'].cat,
                 'strike': o['option'].strike,
                 'direction': o['direction'],
                 'quantity': o['quantity'],
                 'cost': o['option'].cost(o['direction']) * o['quantity']
                } for o in self.options]
    def cost(self):
        return sum(e['option'].cost(e['direction']) * e['quantity'] for e in self.options)


def RatioSpread(call_long, call_short, ratio=None):
    plong = call_long.achat
    pshort = call_short.vente
    ratio = ceil(plong/pshort) if not ratio else ratio
    print('Ratio : {}/{} ~ {}'.format(plong, pshort, ratio))
    return (Strategy('Ratio Spread {}-{} R:{}'.format(call_long.strike, call_short.strike, ratio))
            .add(call_long, 'long', 1)
            .add(call_short, 'short', ratio)
           )


def CallSpread(call_long, call_short):
    """A Call Spread is buy and sell call of different strike:
       - long a call at a strike
       - short a call at a strike superior
    """
    plong = call_long.achat
    pshort = call_short.vente
    return (Strategy('Call Spread {}-{}'.format(call_long.strike, call_short.strike))
            .add(call_long, 'long', 1)
            .add(call_short, 'short', 1)
           )


def PutSpread(put_long, put_short):
    """A Put Spread is buy and sell put of different strike:
       - long a put at a strike
       - short a put at a strike inferior
    """
    plong = put_long.achat
    pshort = put_short.vente
    return (Strategy('Put Spread {}-{}'.format(put_long.strike, put_short.strike))
            .add(put_long, 'long', 1)
            .add(put_short, 'short', 1)
           )


def BoxSpread(call_long, call_short, put_long, put_short):
    """A Box Spread is buy and sell put and call of different strike:
       - short a put at a strike
       - long a put at a strike inferior
       This a strategy of hedgin not speculatif
    """
    plong = call_long.achat
    pshort = call_short.vente
    plong = put_long.achat
    pshort = put_short.vente
    return (Strategy('Box Spread {}-{}'.format(put_long.strike, put_short.strike))
            .add(call_long, 'short', 1)
            .add(call_short, 'long', 1)
            .add(put_long, 'short', 1)
            .add(put_short, 'long', 1)
           )


def IronCondor(put_k1, put_k2, call_k3, call_k4):
    """An Iron Condor is buy and sell put of different strike:
       - short put spread 90/80 permet d'encaisser 2.75
       - short call spread 110/120 permet d'encaisser 3.11
       That is equivalent to:
       - short a put at a strike (90)
       - long a put at a strike inferior (80)
       - short a call at a strike (110)
       - long a call at a strike superior (120)
       The spread strike must be the same
    """
    label = ('Iron Condor {}/{} - {}/{}'
             .format(put_k1.strike, put_k2.strike, call_k3.strike, call_k4.strike)
            )
    label = 'Iron Condor'
    return (Strategy(label)
            .add(put_k1, 'short', 1)
            .add(put_k2, 'long', 1)
            .add(call_k3, 'short', 1)
            .add(call_k4, 'long', 1)
           )
