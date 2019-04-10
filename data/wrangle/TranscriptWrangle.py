'''

'''

import pandas as pd
import gc


def get_offer_id(data):
    try:
        return data['offer id']
    except KeyError:
        try:
            return data['offer_id']
        except:
            return ''


def get_reward(data):
    try:
        return data['reward']
    except KeyError:
        return 0


def get_amount(data):
    try:
        return data['amount']
    except KeyError:
        return 0


def get_duration(offer_id):
    portfolio = pd.read_json('../portfolio.json', orient='records', lines=True)
    if offer_id.strip() != '':
        return portfolio[portfolio.id == offer_id]['duration'].values[0]
    else:
        return 0


def clean_transcript(transcript_clone):
    '''
        Create dummy columns out of event column
    '''
    transcript_clone = pd.get_dummies(transcript_clone, columns=['event'])

    transcript_clone.rename(columns={'event_offer completed': 'offer_completed',
                                     'event_offer received': 'offer_received',
                                     'event_offer viewed': 'offer_viewed',
                                     'event_transaction': 'transaction'},
                            inplace=True)

    '''
        "value" column is a composite column that contains Offer ID, Reward and Amount information. We will extract 
        information into individual columns
    '''
    transcript_clone['offer_id'] = transcript_clone.value.apply(get_offer_id)
    transcript_clone['reward'] = transcript_clone.value.apply(get_reward)
    transcript_clone['amount'] = transcript_clone.value.apply(get_amount)

    transcript_clone.drop(columns=['value'], inplace=True)

    transcript_clone = transcript_clone[
        ['person', 'time', 'offer_id', 'offer_received', 'offer_viewed', 'offer_completed',
         'transaction', 'reward', 'amount']]

    '''
        When an individual has utilized an offer, there are two transactions records created, one for claiming the 
        reward another for making the purchase. We are going to consolidate these two transaction records into one.
    '''
    transcript_clean = transcript_clone.groupby(['person', 'time'], as_index=False).agg('max')

    '''
         Each offer is valid only for a certain number of days once received. In the current data frame, we do not 
         have this information. For successful completion of the offer, the offer should be utilized before expiration.
    '''
    transcript_clean['duration'] = transcript_clean[transcript_clean.offer_received == 1].offer_id.apply(get_duration)

    transcript_clean.duration.fillna(0, inplace=True)

    transcript_clean['duration'] = transcript_clean.duration.apply(lambda x: x * 24)

    transcript_clean['expiration'] = transcript_clean.time + transcript_clean.duration

    transcript_clean.drop(columns='duration', inplace=True)

    transcript_clean = transcript_clean[['person', 'time', 'expiration', 'offer_id', 'offer_received', 'offer_viewed',
                                         'offer_completed', 'transaction', 'reward', 'amount']]

    transcript_clean['expiration'] = transcript_clean.expiration.astype(int)

    '''
        From the above output, it looks like we have populated the transactions that are not offer received with the 
        transaction timestamp. We need to fill with correct offer expiration time if offer id exists.
    '''
    idx = transcript_clean[transcript_clean.offer_received == 0].index

    transcript_clean['expiration'].iloc[idx] = None

    transcript_clean.expiration = transcript_clean.expiration.fillna(value=transcript_clean.time)

    transcript_clean['expiration'] = transcript_clean.expiration.astype(int)

    idx = transcript_clean[(transcript_clean.offer_id != '')
                           & (transcript_clean.offer_received == 0)].index

    transcript_clean['expiration'].iloc[idx] = None

    transcript_clean.expiration = transcript_clean.expiration.fillna(method='ffill')

    transcript_clean['expiration'] = transcript_clean.expiration.astype(int)

    '''
        We will use time columns information to create new columns: offer_received_time, offer_viewed_time, 
        offer_completed_time
    '''
    transcript_clean['offer_received_time'] = transcript_clean[transcript_clean.offer_received == 1]['time']

    transcript_clean['offer_viewed_time'] = transcript_clean[transcript_clean.offer_viewed == 1]['time']

    transcript_clean['offer_completed_time'] = transcript_clean[transcript_clean.offer_completed == 1]['time']

    transcript_clean.offer_received_time.fillna(0, inplace=True)
    transcript_clean.offer_viewed_time.fillna(0, inplace=True)
    transcript_clean.offer_completed_time.fillna(0, inplace=True)

    '''
         A person can receive the same offer multiple times. To consolidate transaction records associated within 
         offer expiration time, we will create a new column "offerid_expiration" and use this column to group the 
         transactions.
    '''
    transcript_clean['offerid_expiration'] = ''

    idx = transcript_clean[transcript_clean.offer_id != ''].index

    transcript_clean['expiration'] = transcript_clean.expiration.astype(str)

    transcript_clean['offerid_expiration'].iloc[idx] = transcript_clean['offer_id'].iloc[idx] + \
                                                       transcript_clean['expiration'].iloc[idx]

    transcript_clean['expiration'] = transcript_clean.expiration.astype(int)

    '''
        Consolidate transaction records associated within offer expiration time
    '''
    transcript_time = transcript_clean.groupby(['person', 'offerid_expiration'], as_index=False)[['amount',
                                                                                                  'offer_id',
                                                                                                  'offer_received_time',
                                                                                                  'offer_viewed_time',
                                                                                                  'offer_completed_time']].max()

    transcript_clean.drop(columns=['offer_received_time', 'offer_viewed_time', 'offer_completed_time'],
                          inplace=True)

    transcript_clean = transcript_clean.merge(transcript_time,
                                              left_on=['person', 'offerid_expiration'],
                                              right_on=['person', 'offerid_expiration'],
                                              how='outer')

    transcript_clean.fillna(0, inplace=True)

    transcript_clean = transcript_clean.sort_values(by=['person', 'time'])

    transcript_clean.drop(columns=['offerid_expiration', 'offer_id_y'], inplace=True)

    transcript_clean.rename(columns={'offer_id_x': 'offer_id'}, inplace=True)

    '''
        We still have different transaction records for viewing/ completing. We will remove rows these rows as have 
        already captured this information in offer received transaction.
    '''
    idx = transcript_clean[(transcript_clean.offer_id != '') & (transcript_clean.offer_received == 0)].index

    transcript_clean.drop(labels=idx, inplace=True)
    transcript_clean.reset_index(inplace=True, drop=True)

    '''
        When we consolidated the transactions, for purchases that were performed without coupon, "amount_y" column is 
        populated by maximum amount spent by the person. We need to correct this.
    '''
    transcript_clean['amount'] = transcript_clean[transcript_clean.offer_id == '']['amount_x']

    transcript_clean['amount'] = transcript_clean.amount.fillna(value=transcript_clean.amount_y)

    transcript_clean.drop(columns=['amount_x', 'amount_y'], inplace=True)

    '''
         For regular transactions, we still have the expiration column populated. We will fill the expiration with 0.
    '''
    idx = transcript_clean[transcript_clean.offer_id == ''].index

    transcript_clean['expiration'].iloc[idx] = 0

    '''
        A user is deemed to be influenced by promotion only after the individual made a transaction after viewing the 
        advertisement. We will create a new column and populate if the promotion or not influence the individual. 
    '''
    idx = transcript_clean[(transcript_clean.offer_viewed_time > 0)
                           & (transcript_clean.offer_viewed_time > transcript_clean.offer_received_time)
                           & (transcript_clean.offer_completed_time > transcript_clean.offer_viewed_time)].index

    transcript_clean['influenced'] = 0

    transcript_clean['influenced'].iloc[idx] = 1

    '''
        Create a new column to capture transaction time.
    '''
    transcript_clean['offer_received_time'] = transcript_clean.offer_received_time.astype(int)
    transcript_clean['offer_viewed_time'] = transcript_clean.offer_viewed_time.astype(int)
    transcript_clean['offer_completed_time'] = transcript_clean.offer_completed_time.astype(int)

    transcript_clean['transaction_time'] = 0

    idx = transcript_clean[transcript_clean.transaction == 1].index

    transcript_clean['transaction_time'].iloc[idx] = transcript_clean['time'].iloc[idx]

    idx = transcript_clean[transcript_clean.transaction == 0].index

    transcript_clean['transaction_time'].iloc[idx] = transcript_clean['offer_completed_time'].iloc[idx]

    '''
        When the transactions are consolidated, we lost information about  offer_received, offer_viewed, 
        offer_completed columns. We need to populate with correct values.
    '''

    transcript_clean['offer_received'] = 0

    idx = transcript_clean[transcript_clean.offer_received_time > 0].index

    transcript_clean['offer_received'].iloc[idx] = 1

    transcript_clean['offer_viewed'] = 0

    idx = transcript_clean[transcript_clean.offer_viewed_time > 0].index

    transcript_clean['offer_viewed'].iloc[idx] = 1

    transcript_clean['offer_completed'] = 0

    idx = transcript_clean[transcript_clean.offer_completed_time > 0].index

    transcript_clean['offer_completed'].iloc[idx] = 1

    transcript_clean = transcript_clean[['person', 'offer_id', 'time', 'offer_received_time', 'offer_viewed_time',
                                         'offer_completed_time', 'transaction_time', 'expiration', 'offer_received',
                                         'offer_viewed', 'offer_completed', 'transaction', 'reward', 'amount',
                                         'influenced']]

    '''
        We no longer need "time" and "expiration" information. We will drop these columns.
    '''
    transcript_clean.drop(columns=['time', 'expiration'], inplace=True)

    del transcript_clone
    del transcript_time
    gc.collect()

    return transcript_clean
