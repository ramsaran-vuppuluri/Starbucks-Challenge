'''

'''

import pandas as pd


def consolidate_to_transaction_without_dummies(transcript_clean, profile_for_ml, portfolio_for_ml):
    transaction = transcript_clean.groupby(['person', 'offer_id'], as_index=False).sum()

    transaction.influenced.replace(to_replace=2, value=1, inplace=True)
    transaction.influenced.replace(to_replace=3, value=1, inplace=True)

    transaction.drop(columns=['offer_received_time', 'offer_viewed_time', 'offer_completed_time',
                              'transaction_time'],
                     inplace=True)

    transaction = transaction.merge(profile_for_ml, left_on='person', right_on='id')

    transaction.drop(columns=['person', 'id'], inplace=True)

    transaction = transaction.merge(portfolio_for_ml, left_on=['offer_id'], right_on=['id'], how='left')

    transaction.drop(columns=['offer_received', 'offer_viewed', 'offer_completed', 'transaction', 'offer_id', 'id',
                              'reward_y'],
                     inplace=True)

    transaction.fillna(0, inplace=True)

    transaction[['difficulty', 'duration', 'bogo', 'discount', 'informational', 'email', 'mobile', 'social', 'web',
                 'offer_code']] = transaction[
        ['difficulty', 'duration', 'bogo', 'discount', 'informational', 'email', 'mobile', 'social', 'web',
         'offer_code']].astype(int)

    transaction.rename(columns={'reward_x': 'reward'}, inplace=True)

    return transaction


def consolidate_to_transaction(transcript_clean, profile_for_ml, portfolio_for_ml):
    transaction = consolidate_to_transaction_without_dummies(transcript_clean, profile_for_ml, portfolio_for_ml)

    transaction = pd.get_dummies(transaction, columns=['offer_code'])

    transaction = transaction[['age', 'income', 'gender_F', 'gender_M', 'gender_O', 'became_member_on_year',
                               'became_member_on_month', 'became_member_on_date', 'difficulty', 'duration',
                               'bogo', 'discount', 'informational', 'email', 'mobile', 'social', 'web', 'reward',
                               'amount', 'influenced', 'offer_code_0', 'offer_code_1', 'offer_code_2', 'offer_code_3',
                               'offer_code_4', 'offer_code_5', 'offer_code_6', 'offer_code_7', 'offer_code_8',
                               'offer_code_9', 'offer_code_10']]

    return transaction
