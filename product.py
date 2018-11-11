import numpy as np


class Option:
    def __init__(self, cat='Call', strike=0, achat=0, vente=0, multiplier=1):
        self.cat = cat
        self.strike = strike
        self.achat = achat
        self.vente = vente
        self.multiplier = multiplier
    def __repr__(self):
        #return '{}({}, {}, {})'.format(self.cat, self.strike, self.achat, self.vente)
        return '{}({})'.format(self.cat, self.strike)
    def __str__(self):
        return '{}({}) long:{}, short:{}'.format(self.cat, self.strike, self.achat, self.vente)
    def payoff_long(self, sT):
        return self._payoff(sT, self.achat, self.multiplier)
    def payoff_short(self, sT):
        return self._payoff(sT, self.vente, self.multiplier * -1)
    def _payoff(self, sT, premium, multiplier):
        if self.cat == 'Call':
            return (np.where(sT > self.strike, sT - self.strike, 0) - premium) * multiplier
        elif self.cat == 'Put':
            return (np.where(sT < self.strike, self.strike - sT, 0) - premium) * multiplier
    def payoff(self, sT, direction):
        if direction == 'long':
            return self.payoff_long(sT)
        elif direction == 'short':
            return self.payoff_short(sT)
        raise Exception('direction not good {}'.format(direction))
    def cost(self, direction):
        if direction == 'long':
            return self.multiplier * self.achat
        elif direction == 'short':
            return -self.multiplier * self.vente
        raise Exception('direction not good {}'.format(direction))

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
    def cost(self):
        return sum(e['option'].cost(e['direction']) * e['quantity'] for e in self.options)
