# Starbucks-Challenge

### Introduction
This data set contains simulated data that mimics customer behavior on the Starbucks rewards mobile app. Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offer during certain weeks.

Not all users receive the same offer, and that is the challenge to solve with this data set.

Every offer has a validity period before the offer expires. As an example, a BOGO offer might be valid for only 5 days. You'll see in the data set that informational offers have a validity period even though these ads are merely providing information about a product; for example, if an informational offer has 7 days of validity, you can assume the customer is feeling the influence of the offer for 7 days after receiving the advertisement.

To give an example, a user could receive a discount offer buy 10 dollars get 2 off on Monday. The offer is valid for 10 days from receipt. If the customer accumulates at least 10 dollars in purchases during the validity period, the customer completes the offer.

However, there are a few things to watch out for in this data set. Customers do not opt into the offers that they receive; in other words, a user can receive an offer, never actually view the offer, and still complete the offer. For example, a user might receive the "buy 10 dollars get 2 dollars off offer", but the user never opens the offer during the 10 day validity period. The customer spends 15 dollars during those ten days. There will be an offer completion record in the data set; however, the customer was not influenced by the offer because the customer never viewed the offer.

### Project Structure:
    
    |
    |--- app                            <- Contains the source code to run Web Application.
    |   |
    |   |--- templates                  <- Contains HTML files used in the Web Application.
    |   |   |
    |   |   |--- index.html             <- Landing page for the Web Application.
    |   |   |
    |   |   |--- predict_amt.html       <- Web page to get predicted total amount value.
    |   |
    |   |--- run.py                     <- Python script with Flask code to route HTTP requests.
    |
    |--- data                           <- Contains Data wrangling and analysis source code. 
    |   |
    |   |--- analyze                    <- Contains Data analysis source code.
    |   |   |
    |   |   |--- analyze.py             <- Python script with Plotly code to generate ad-hoc visualizations.
    |   |
    |   |--- wrangle                    <- Contains Data wrangling source code.
    |   |   |
    |   |   |--- Consolidate.py         <- Python script to consolidated all three clean data sources into one consolidated data source.
    |   |   |
    |   |   |--- PortifolioWrangle.py   <- Python utility script with code wrangle Portfolio data.
    |   |   |
    |   |   |--- ProfileWrangle.py      <- Python utility script with code wrangle Profile data.
    |   |   |
    |   |   |--- TranscriptWrangle.py   <- Python utility script with code wrangle Transcript data.
    |   |   |
    |   |   |--- Wrangle.py             <- Python script to wrangle all three data sources.
    |   |
    |   |--- portfolio.json             <- Simulated portfolio data provided by Starbucks
    |   |
    |   |--- portfolio_for_ml.csv       <- Pivoted portfolio data is stored in CSV format.
    |   |
    |   |--- profile.json               <- Simulated profile data provided by Starbucks
    |   |
    |   |--- profile_for_ml.csv         <- Pivoted profile data is stored in CSV format.
    |   |
    |   |--- transaction.csv            <- Pivoted transcript data is stored in CSV format.
    |   |
    |   |--- transcript.json            <- Simulated transcript data provided by Starbucks
    |   |       
    |   |--- transcript_clean.csv       <- Pivoted transcript data is stored in CSV format.
    |
    |--- model
    |   |
    |   |--- amount_clf.joblib          <- Pretrained sklearn model is stored for predictions.
    |   |
    |   |--- influnce_clf.joblib        <- Pretrained sklearn model is stored for predictions.
    |   |
    |   |--- offer_code_clf.joblib      <- Pretrained sklearn model is stored for predictions.
    |   |
    |   |--- predict.py                 <- Python script to predict values based on pretrained models.
    |   |
    |   |--- train.py                   <- Python script to train models to training data.
    |
    |--- CRISP-DM_Process_Diagram.png   <- Image resource for Jupyter notebook.
    |
    |--- pic1.png                       <- Image resource for Jupyter notebook.
    |
    |--- pic2.png                       <- Image resource for Jupyter notebook.
    |
    |--- LICENSE                        <- MIT distribution license.
    |
    |--- Starbucks_Challenge.ipynb      <- Jupyter notebook with source code.
    |
    |--- Starbucks_Challenge.html       <- Jupyter notebook HTML snapshot.
    
### Instructions:
1. Run the following command in the app's directory to run your web app.
    `python run.py`

2. Go to http://0.0.0.0:3001/

### Libraries
    | Library       | Version   |
    | ------------- |-----------|
    |Flask          | 0.12.2    |
    |joblib         | 0.13.2    |
    |Pandas         | 0.22.0    |
    |sklearn        | 0.19.1    |
    |Bootstrap      | 3.x       |
    |Plotly         | 3.6.1     |
