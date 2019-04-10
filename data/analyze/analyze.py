from data.wrangle.Wrangle import Wrangle

import plotly.graph_objs as go

import pandas as pd


def get_transcript_by_person():
    transcript_clean = pd.read_csv('../data/transcript_clean.csv')

    transcript_by_person = transcript_clean.groupby('person', as_index=False).sum()

    transcript_by_person.drop(columns=['offer_received_time', 'offer_viewed_time', 'offer_completed_time',
                                       'transaction_time'],
                              inplace=True)

    profile = profile = pd.read_json('../data/profile.json', orient='records', lines=True)

    transcript_by_person = profile.merge(transcript_by_person, left_on='id', right_on='person')

    transcript_by_person.drop(columns=['id', 'person'], inplace=True)

    return transcript_by_person, profile


def get_event_by_gender(transcript_by_person):
    event_by_gender = transcript_by_person.groupby('gender', as_index=False)[['offer_completed', 'offer_received',
                                                                              'offer_viewed', 'transaction',
                                                                              'influenced']].sum()

    event_by_gender.gender.replace(to_replace='F', value='Female', inplace=True)
    event_by_gender.gender.replace(to_replace='M', value='Male', inplace=True)
    event_by_gender.gender.replace(to_replace='O', value='Other', inplace=True)

    trace0 = go.Bar(x=event_by_gender.gender,
                    y=event_by_gender.offer_received,
                    text=event_by_gender.offer_received,
                    textposition='auto',
                    name='Offer Received',
                    marker=dict(color='rgba(0,107,164,1)', ))

    trace1 = go.Bar(x=event_by_gender.gender,
                    y=event_by_gender.offer_viewed,
                    text=event_by_gender.offer_viewed,
                    textposition='auto',
                    name='Offer Viewed',
                    marker=dict(color='rgba(255,128,14,1)', ))

    trace2 = go.Bar(x=event_by_gender.gender,
                    y=event_by_gender.offer_completed,
                    text=event_by_gender.offer_completed,
                    textposition='auto',
                    name='Offer Completed',
                    marker=dict(color='rgba(171,171,171,1)', ))

    trace3 = go.Bar(x=event_by_gender.gender,
                    y=event_by_gender.transaction,
                    text=event_by_gender.transaction,
                    textposition='auto',
                    name='Transaction',
                    marker=dict(color='rgba(89,89,89,1)', ))

    trace4 = go.Bar(x=event_by_gender.gender,
                    y=event_by_gender.influenced,
                    text=event_by_gender.influenced,
                    textposition='auto',
                    name='Influenced',
                    marker=dict(color='rgba(95,158,209,1)', ))

    layout = go.Layout(
        title='Event Distribution by Gender',
        barmode='group',
        bargap=0.15
    )

    data = [trace0, trace1, trace2, trace3, trace4]

    return data, layout


def get_events_by_age(transcript_by_person):
    trace0 = go.Scatter(x=transcript_by_person.age,
                        y=transcript_by_person.offer_received,
                        name='Offer Received',
                        mode='markers',
                        marker=dict(color='rgba(0,107,164,1)', ))

    trace1 = go.Scatter(x=transcript_by_person.age,
                        y=transcript_by_person.offer_viewed,
                        name='Offer Viewed',
                        mode='markers',
                        marker=dict(color='rgba(255,128,14,1)', ))

    trace2 = go.Scatter(x=transcript_by_person.age,
                        y=transcript_by_person.offer_completed,
                        name='Offer Completed',
                        mode='markers',
                        marker=dict(color='rgba(171,171,171,1)', ))

    trace3 = go.Scatter(x=transcript_by_person.age,
                        y=transcript_by_person.transaction,
                        name='Transaction',
                        mode='markers',
                        marker=dict(color='rgba(89,89,89,1)', ))

    trace4 = go.Scatter(x=transcript_by_person.age,
                        y=transcript_by_person.influenced,
                        name='Influenced',
                        mode='markers',
                        marker=dict(color='rgba(95,158,209,1)', ))

    data = [trace0, trace1, trace2, trace3, trace4]

    layout = go.Layout(
        title='Event Distribution by Age',
        bargap=0.15
    )

    return data, layout


def get_event_by_income(transcript_by_person, profile):
    event_by_income = transcript_by_person.groupby('income', as_index=False)[['offer_completed', 'offer_received',
                                                                              'offer_viewed', 'transaction',
                                                                              'influenced']].sum()

    trace0 = go.Scatter(x=event_by_income.income,
                        y=event_by_income.offer_received,
                        name='Offer Received',
                        marker=dict(color='rgba(0,107,164,1.25)', ))

    trace1 = go.Scatter(x=event_by_income.income,
                        y=event_by_income.offer_viewed,
                        name='Offer Viewed',
                        marker=dict(color='rgba(255,128,14,1.25)', ))

    trace2 = go.Scatter(x=event_by_income.income,
                        y=event_by_income.offer_completed,
                        name='Offer Completed',
                        marker=dict(color='rgba(200,82,0,1.25)', ))

    trace3 = go.Scatter(x=event_by_income.income,
                        y=event_by_income.transaction,
                        name='Transaction',
                        marker=dict(color='rgba(89,89,89,1.25)', ))

    trace4 = go.Scatter(x=event_by_income.income,
                        y=event_by_income.influenced,
                        name='Influenced',
                        marker=dict(color='rgba(95,158,209,1.25)', ))

    trace = go.Histogram(x=profile.income.values,
                         name='Income',
                         marker=dict(color='rgba(95,158,209,0.15)', ),
                         yaxis='y2')

    data = [trace0, trace1, trace2, trace3, trace4, trace]

    layout = go.Layout(
        title='Event Distribution by Income',
        yaxis2=dict(
            overlaying='y',
            side='right'
        )
    )

    return data, layout


def get_events():
    transcript_by_person, profile = get_transcript_by_person()

    data1, layout1 = get_event_by_gender(transcript_by_person)

    data2, layout2 = get_events_by_age(transcript_by_person)

    data3, layout3 = get_event_by_income(transcript_by_person, profile)

    graphs = [
        {
            'data': data1,
            'layout': layout1
        },
        {
            'data': data2,
            'layout': layout2
        },
        {
            'data': data3,
            'layout': layout3
        }
    ]

    return graphs


def get_offer_ids():
    portfolio = pd.read_csv('../data/portfolio_for_ml.csv')
    return portfolio.id.values
