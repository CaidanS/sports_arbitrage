import imp
from scipy import interpolate
from datetime import datetime
from dateutil import parser

m_price = interpolate.interp1d([0, 10], [0,1])
m_size = interpolate.interp1d([0, 1000], [0,1])
m_date = interpolate.interp1d([0, 365], [0,1])
m_cancel = interpolate.interp1d([0, 3], [0,1])

bookmaker_risk_profiles = {
    # 'williamhill_us': {
    #     'bet_amount': lambda bet_amount :,
    #     'price': 10,
    #     'commence_date': 1
    # }
    'default_risk_profile': {
        'bet_amount': lambda bet_amount : m_size(bet_amount) * 10,
        'price': lambda price : m_price(price) * 8,
        'commence_date': lambda date: m_date((parser.parse(date) - datetime.utcnow()).days + 1) ** .2
    }
}

def calc_likelihood_of_cancellation(bookmaker_key, bet_amount, price, commence_date):
    likelihood_of_cancellation = 0
    if bookmaker_key in bookmaker_risk_profiles.keys():
        likelihood_of_cancellation += bookmaker_risk_profiles[bookmaker_key]['bet_amount'](bet_amount)
        likelihood_of_cancellation += bookmaker_risk_profiles[bookmaker_key]['price'](price)
        likelihood_of_cancellation += bookmaker_risk_profiles[bookmaker_key]['commence_date'](commence_date)
    else:
        likelihood_of_cancellation += bookmaker_risk_profiles['default_risk_profile']['bet_amount'](bet_amount)
        likelihood_of_cancellation += bookmaker_risk_profiles['default_risk_profile']['price'](price)
        likelihood_of_cancellation += bookmaker_risk_profiles['default_risk_profile']['commence_date'](commence_date)
    print(likelihood_of_cancellation)
    return m_cancel(likelihood_of_cancellation)