import json
import plotly

import pandas as pd

from flask import Flask
from flask import render_template, request

from data.analyze.analyze import get_events, get_offer_ids
from model.predict import predict_amount

app = Flask(__name__)

graphs = get_events()

offer_ids = list(get_offer_ids())
offer_ids.append(' ')


@app.route('/')
@app.route('/index')
def index():
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    # render web page with plotly graphs
    return render_template('index.html', ids=ids, graphJSON=graphJSON)


@app.route('/predict_amt')
def predict_amt():
    # render web page with plotly graphs
    return render_template('predict_amt.html', offer_ids=offer_ids)


@app.route('/go')
def go():
    age = request.args.get('age', '')
    income = request.args.get('income', '0')
    gender = request.args.get('gender', '')
    became_member_on = request.args.get('became_member_on', '2018-01-01')
    offer_id = request.args.get('offer_id', '')

    age = int(age)

    if income == '':
        income = 50000.00
    else:
        income = float(income)

    amount = predict_amount(age, income, gender, became_member_on, offer_id)

    amount = "Predicted Total Purchase Amount is {0}".format(amount)

    print(amount)

    return render_template('predict_amt.html', offer_ids=offer_ids, amount=amount)


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
