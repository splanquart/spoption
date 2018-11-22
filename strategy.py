import numpy as np
from math import ceil, floor


class Strategy:
    def __init__(self, label=''):
        self.label = label
        self.options = []

    def add(self, option, direction, quantity):
        self.options.append({'option': option,
                             'direction': direction,
                             'quantity': quantity})
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
    """
    RatioSpread
    .................
    .     /\        .
    . ___/  \       .
    .        \_____ .
    .................
    """
    plong = call_long.achat
    pshort = call_short.vente
    ratio = ceil(plong/pshort) if not ratio else ratio
    print('Ratio : {}/{} ~ {}'.format(plong, pshort, ratio))
    return (Strategy('Ratio Spread {}-{} R:{}'.format(call_long.strike, call_short.strike, ratio))
            .add(call_long, 'long', 1)
            .add(call_short, 'short', ratio)
            )


class CallSpread(Strategy):
    """A Call Spread is buy and sell call of different strike:
       - long a call at a strike
       - short a call at a strike superior
       .................
       .       _______ .
       .      /        .
       .     /         .
       .____/          .
       .................
    """
    def __init__(self, call_long, call_short):
        """ Create a Call spread
        call_long.strike < call_short.strike

        >>> cs = CallSpread(call[100], call[120])
        """
        plong = call_long.achat
        pshort = call_short.vente
        super().__init__('Call Spread {}-{}'.format(call_long.strike, call_short.strike))
        self.add(call_long, 'long', 1)
        self.add(call_short, 'short', 1)

    @staticmethod
    def explorator(list_put, step=50):
        strikes = [o.strike for o in list_put]
        by_strike = dict(zip(strikes, list_put))
        css = []
        for i, strike_a in enumerate(strikes[:-1]):
            strike_b = strike_a + step
            if (strike_b not in strikes):
                continue
            a = by_strike[strike_a]
            b = by_strike[strike_b]
            css.append(CallSpread(a, b))
        return css


class PutSpread(Strategy):
    """A Put Spread is buy and sell put of different strike:
       - long a put at a strike
       - short a put at a strike inferior
       .................
       . _____         .
       .      \        .
       .       \       .
       .        \_____ .
       .................
       - put_long.strike > put_short.strike

       >>> ps = PutSpread(put[100], put[80])
    """
    def __init__(self, put_long, put_short):
        plong = put_long.achat
        pshort = put_short.vente
        super().__init__('Put Spread {}-{}'.format(put_long.strike, put_short.strike))
        self.add(put_long, 'long', 1)
        self.add(put_short, 'short', 1)

    @staticmethod
    def explorator(list_put, step=50):
        strikes = [o.strike for o in list_put]
        by_strike = dict(zip(strikes, list_put))
        pss = []
        for i, strike_a in enumerate(strikes[:-1]):
            strike_b = strike_a + step
            if (strike_b not in strikes):
                continue
            a = by_strike[strike_a]
            b = by_strike[strike_b]
            pss.append(PutSpread(b, a))
        return pss


class BoxSpread(Strategy):
    """A Box Spread is buy and sell put and call of different strike:
       - short a put at a strike
       - long a put at a strike inferior
       This a strategy of hedgin not speculatif
       .....................
       .       _____       .
       .      /     \      .
       .     /       \     .
       . ___/         \___ .
       .....................
    """
    def __init__(self, call_long, call_short, put_long, put_short):
        plong = call_long.achat
        pshort = call_short.vente
        plong = put_long.achat
        pshort = put_short.vente
        super().__init__('Box Spread {}-{}'.format(call_long.strike, put_short.strike))
        self.add(call_long, 'short', 1)
        self.add(call_short, 'long', 1)
        self.add(put_long, 'short', 1)
        self.add(put_short, 'long', 1)

    @staticmethod
    def explorator(list_call, list_put, spread=50, gap=100, step=25):
        """
        :param: spread diff between strike of 2 call or 2 put
        :param: gap diff between put and call
        :param: step diff between 2 BoxSpread
        """
        strikes_call = [o.strike for o in list_call]
        strikes_put = [o.strike for o in list_put]
        strikes = [v for v in strikes_call if v in strikes_put]
        strikes = strikes_call + strikes_put
        call_by_strike = dict(zip(strikes, list_call))
        put_by_strike = dict(zip(strikes, list_call))

        bfs = []
        for i, strike_a in enumerate(strikes[:-3]):
            strike_b = strike_a + step
            strike_c = strike_b + gap
            strike_d = strike_c + step
            if (strike_a not in call_by_strike or
                strike_b not in call_by_strike or
                strike_c not in put_by_strike or
                strike_d not in put_by_strike
                ):
                continue
            a = call_by_strike[strike_a]
            b = call_by_strike[strike_b]
            c = put_by_strike[strike_c]
            d = put_by_strike[strike_d]
            bfs.append(BoxSpread(b, a, c, d))
        return bfs


class Butterfly(Strategy):
    """A Butterfly is buy 2 call strike K et K+2 and sell two call of strike K+1:
       - long a call at a strike K
       - short two calls at a strike K+1
       - long a call at a strike K+2
       .................
       .      /\       .
       .     /  \      .
       .    /    \     .
       .___/      \___ .
       .................
    """
    def __init__(self, call_low, call_middle, call_high, label=None):
        label = 'Butterfly {}-2*{}+{}'.format(call_low.strike,
                                              call_middle.strike,
                                              call_high.strike)
        super().__init__(label)
        self.add(call_low, 'long', 1)
        self.add(call_middle, 'short', 2)
        self.add(call_high, 'long', 1)

    @staticmethod
    def explorator(list_call, step=50):
        strikes = [o.strike for o in list_call]
        by_strike = dict(zip(strikes, list_call))
        bfs = []
        for i, strike_a in enumerate(strikes[:-2]):
            strike_b = strike_a + step
            strike_c = strike_b + step
            if (strike_b not in strikes or
                strike_c not in strikes
                ):
                continue
            a = by_strike[strike_a]
            b = by_strike[strike_b]
            c = by_strike[strike_c]
            bfs.append(Butterfly(a, b, c))
        return bfs


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
    .....................
    .       _____       .
    .      /     \      .
    .     /       \     .
    . ___/         \___ .
    .....................
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
