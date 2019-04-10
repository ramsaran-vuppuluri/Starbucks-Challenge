'''

'''

import pandas as pd


def clean_profile(profile):
    profile.dropna(inplace=True)
    profile['became_member_on'] = pd.to_datetime(profile.became_member_on, format='%Y%m%d')

    return profile


def generate_profile_for_ml(clean_profile):
    profile_for_ml = clean_profile.copy()

    profile_for_ml = pd.get_dummies(profile_for_ml, columns=['gender'])

    profile_for_ml['became_member_on_year'] = profile_for_ml.became_member_on.dt.year
    profile_for_ml['became_member_on_month'] = profile_for_ml.became_member_on.dt.month
    profile_for_ml['became_member_on_date'] = profile_for_ml.became_member_on.dt.day

    profile_for_ml.drop(columns=['became_member_on'], inplace=True)

    return profile_for_ml
