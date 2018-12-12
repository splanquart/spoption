from math import sqrt

def pivot_sr(H, B, C):
    """
    Pivot = (H + B + C) / 3
    S1 = (2 x Pivot) - H
    S2 = Pivot - (H - B)
    S3 = B - 2x (H - Pivot)
    R1 = (2 x Pivot) - B
    R2 = Pivot + (H - B)
    R3 = H + 2x (Pivot - B)
    """
    Pivot = (H + B + C) / 3
    S1 = (2 * Pivot) - H
    S2 = Pivot - (H - B)
    S3 = B - 2 * (H - Pivot)
    R1 = (2 * Pivot) - B
    R2 = Pivot + (H - B)
    R3 = H + 2 * (Pivot - B)
    return {'pivot': Pivot,
            'S1': S1,
            'R1': R1,
            'S2': S2,
            'R2': R2,
            'S3': S3,
            'R3': R3,
            }

def deviation(close, volatility, period, precision=0):
    sd_period = round(sqrt(period / 252) * close * volatility / 100, precision)
    return {
        '1': {'min': close - sd_period,
              'max': close + sd_period},
        '2': {'min': close - 2 * sd_period,
              'max': close + 2 * sd_period},
        'sd': sd_period,
    }

def atm(price, options):
    strikes = [o.strike for o in options]
    atm = round(price / 25, 0) * 25
    doptions = dict(zip(strikes, options))
    return doptions[atm]
