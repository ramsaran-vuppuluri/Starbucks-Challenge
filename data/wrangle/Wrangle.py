'''
    @author Ram SaranVuppuluri.
'''

import pandas as pd
import os

import warnings

warnings.filterwarnings('ignore')

from data.wrangle.PortfolioWrangle import generate_portfolio_for_ml
from data.wrangle.ProfileWrangle import generate_profile_for_ml, clean_profile
from data.wrangle.TranscriptWrangle import clean_transcript
from data.wrangle.Consolidate import consolidate_to_transaction


class Wrangle:
    def __init__(self, portfolio_path='../portfolio.json', profile_path='../profile.json',
                 transcript_path='../transcript.json'):
        print(portfolio_path)
        self.portfolio = pd.read_json(portfolio_path, orient='records', lines=True)
        self.profile = pd.read_json(profile_path, orient='records', lines=True)
        self.transcript = pd.read_json(transcript_path, orient='records', lines=True)

    def get_profile(self):
        return self.profile

    def get_portfolio(self):
        return self.portfolio

    def get_transcript(self):
        return self.transcript

    def get_portfolio_for_ml(self):
        if os.path.exists('../portfolio_for_ml.csv'):
            portfolio_for_ml = pd.read_csv('../portfolio_for_ml.csv')
        else:
            print("Generating portfolio_for_ml")

            portfolio_for_ml = generate_portfolio_for_ml(self.portfolio)

            print("Writing portfolio_for_ml.csv")

            portfolio_for_ml.to_csv('../portfolio_for_ml.csv', index=False)

        return portfolio_for_ml

    def get_profile_for_ml(self):
        if os.path.exists('../profile_for_ml.csv'):
            profile_for_ml = pd.read_csv('../profile_for_ml.csv')
        else:
            print("Generating profile_for_ml")

            profile_for_ml = generate_profile_for_ml(clean_profile(self.profile))

            print("Writing profile_for_ml.csv")

            profile_for_ml.to_csv('../profile_for_ml.csv', index=False)

        return profile_for_ml

    def get_transcript_clean(self):
        if os.path.exists('../transcript_clean.csv'):
            transcript_clean = pd.read_csv('../transcript_clean.csv')
        else:
            print("Generating transcript_clean")

            transcript_clean = clean_transcript(self.transcript)

            print("Writing transcript_clean.csv")

            transcript_clean.to_csv('../transcript_clean.csv', index=False)
        return transcript_clean

    def get_transaction(self):
        if os.path.exists('../transaction.csv'):
            transaction = pd.read_csv('../transaction.csv')
        else:
            print("Generating transaction")

            transaction = consolidate_to_transaction(self.transcript_clean, self.profile_for_ml, self.portfolio_for_ml)

            print("Writing transaction.csv")

            transaction.to_csv('../transaction.csv', index=False)
        return transaction
