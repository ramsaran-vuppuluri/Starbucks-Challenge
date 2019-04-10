from joblib import load

import pandas as pd

from data.wrangle.Wrangle import Wrangle


def predict_influence(difficulty, reward, amount):
    influnce_clf = load('../model/influnce_clf.joblib')

    data = {'difficulty': [difficulty], 'reward': [reward], 'amount': [amount]}

    x = pd.DataFrame(data, columns=['difficulty', 'reward', 'amount'])

    result = influnce_clf.predict(x)[0]

    if result == 0:
        return "Will not be influenced"
    else:
        return "Will be influenced"


def predict_amount(age, income, gender, became_member_on, offer_id=''):
    amount_clf = load('../model/amount_clf.joblib')

    transaction = prep_input_data(age, became_member_on, gender, income, offer_id)

    return amount_clf.predict(transaction)[0]


def without_valid_offer_id(age, became_member_on, columns, gender, income):
    data = {'age': [age], 'income': [income], 'gender_F': [0], 'gender_M': [0], 'gender_O': [0],
            'became_member_on': [became_member_on], 'offer_code_0': [1]}
    transaction = pd.DataFrame(data,
                               columns=['age', 'income', 'gender_F', 'gender_M', 'gender_O', 'became_member_on',
                                        'offer_code_0'])
    if gender == 'Male':
        transaction['gender_M'] = 1
    elif gender == 'Female':
        transaction['gender_F'] = 1
    else:
        transaction['gender_O'] = 1
    transaction['became_member_on'] = pd.to_datetime(transaction['became_member_on'])
    transaction['became_member_on_year'] = transaction.became_member_on.dt.year
    transaction['became_member_on_month'] = transaction.became_member_on.dt.month
    transaction['became_member_on_date'] = transaction.became_member_on.dt.day
    transaction.drop(columns='became_member_on', inplace=True)
    portfolio_for_ml_cols = ['difficulty', 'duration', 'reward', 'bogo', 'discount', 'informational',
                             'email', 'mobile', 'social', 'web', 'offer_code_1', 'offer_code_2',
                             'offer_code_3', 'offer_code_4', 'offer_code_5', 'offer_code_6',
                             'offer_code_7', 'offer_code_8', 'offer_code_9', 'offer_code_10']
    for col in portfolio_for_ml_cols:
        transaction[col] = 0

    transaction = transaction[columns]

    return transaction


def with_valid_offer_id(age, became_member_on, gender, income, offer_id, columns):
    wrangle = Wrangle(portfolio_path='../data/portfolio.json', profile_path='../data/profile.json',
                      transcript_path='../data/transcript.json')
    transaction = wrangle.get_portfolio_for_ml()

    transaction = pd.get_dummies(transaction, columns=['offer_code'])
    transaction = transaction[transaction.id == offer_id]
    # transaction = transaction.drop(columns=['id'], inplace=True)

    transaction['age'] = age
    transaction['became_member_on'] = became_member_on
    transaction['gender_F'] = 0
    transaction['gender_M'] = 0
    transaction['gender_O'] = 0

    if gender == 'Male':
        transaction['gender_M'] = 1
    elif gender == 'Female':
        transaction['gender_F'] = 1
    else:
        transaction['gender_O'] = 1

    transaction['income'] = income

    transaction['became_member_on'] = pd.to_datetime(transaction['became_member_on'])
    transaction['became_member_on_year'] = transaction.became_member_on.dt.year
    transaction['became_member_on_month'] = transaction.became_member_on.dt.month
    transaction['became_member_on_date'] = transaction.became_member_on.dt.day
    transaction.drop(columns='became_member_on', inplace=True)

    transaction['offer_code_0'] = 0

    transaction = transaction[columns]
    return transaction


def prep_input_data(age, became_member_on, gender, income, offer_id):
    columns = ['age', 'income', 'gender_F', 'gender_M', 'gender_O', 'became_member_on_year', 'became_member_on_month',
               'became_member_on_date', 'difficulty', 'duration', 'bogo', 'discount', 'informational', 'email',
               'mobile', 'social', 'web', 'reward', 'offer_code_0', 'offer_code_1', 'offer_code_2', 'offer_code_3',
               'offer_code_4', 'offer_code_5', 'offer_code_6', 'offer_code_7', 'offer_code_8', 'offer_code_9',
               'offer_code_10']

    if offer_id.strip() != '':
        return with_valid_offer_id(age, became_member_on, gender, income, offer_id, columns)
    else:
        return without_valid_offer_id(age, became_member_on, columns, gender, income)
