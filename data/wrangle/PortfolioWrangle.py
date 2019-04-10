'''

'''

import pandas as pd

def channels_mobile(data):
    if 'mobile' in data:
        return 1
    else:
        return 0

def channels_email(data):
    email, mobile, social, web = 0, 0, 0, 0
    if 'email' in data:
        return 1
    else:
        return 0

def channels_social(data):
    if 'social' in data:
        return 1
    else:
        return 0

def channels_web(data):
    if 'web' in data:
        return 1
    else:
        return 0

def generate_portfolio_for_ml(portfolio):
    portfolio_for_ml = pd.get_dummies(portfolio, columns=['offer_type'])

    portfolio_for_ml.rename(columns={'offer_type_bogo': 'bogo',
                                     'offer_type_discount': 'discount',
                                     'offer_type_informational': 'informational'},
                            inplace=True)

    portfolio_for_ml['email'] = portfolio_for_ml.channels.apply(lambda x: channels_email(x))
    portfolio_for_ml['mobile'] = portfolio_for_ml.channels.apply(lambda x: channels_mobile(x))
    portfolio_for_ml['social'] = portfolio_for_ml.channels.apply(lambda x: channels_social(x))
    portfolio_for_ml['web'] = portfolio_for_ml.channels.apply(lambda x: channels_web(x))

    portfolio_for_ml.drop(columns=['channels'], inplace=True)
    portfolio_for_ml['offer_code'] = (portfolio_for_ml.index.values + 1)

    return portfolio_for_ml
