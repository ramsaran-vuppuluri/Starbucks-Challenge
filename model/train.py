''''
'''

from joblib import dump
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingRegressor
from sklearn.metrics import make_scorer, f1_score, classification_report, accuracy_score, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline, make_union
from sklearn.preprocessing import StandardScaler

from data.wrangle.Consolidate import consolidate_to_transaction_without_dummies
from data.wrangle.Wrangle import Wrangle


def train_for_influence():
    wrangle = Wrangle()

    transaction = wrangle.get_transaction()

    features = transaction.columns.drop(['influenced'])

    features = transaction.columns.drop(['age', 'income', 'gender_F', 'gender_M', 'gender_O', 'became_member_on_year',
                                         'became_member_on_month', 'became_member_on_date', 'duration', 'bogo',
                                         'discount', 'informational', 'email', 'mobile', 'social', 'web', 'influenced',
                                         'offer_code_0', 'offer_code_1', 'offer_code_2', 'offer_code_3', 'offer_code_4',
                                         'offer_code_5', 'offer_code_6', 'offer_code_7', 'offer_code_8', 'offer_code_9',
                                         'offer_code_10'])

    X = transaction[features]
    y = transaction['influenced']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # This code snippet is for running all grid combination.
    # numerical_columns = ['age', 'income', 'became_member_on_year', 'became_member_on_month', 'became_member_on_date',
    #                      'difficulty', 'duration', 'reward', 'amount']
    # transformer = make_union(StandardScaler())
    #
    # clf = RandomForestClassifier()
    #
    # pipeline = Pipeline([
    #     ('classifier', clf)
    # ])
    #
    # parameters = [
    #     {
    #         "classifier__n_estimators": range(10, 110, 10)
    #     },
    #     {
    #         "classifier": [AdaBoostClassifier()],
    #         "classifier__n_estimators": range(10, 110, 10),
    #         "classifier__learning_rate": np.linspace(0.1, 2.5, 20)
    #     },
    #     {
    #         "classifier": [ExtraTreesClassifier()],
    #         "classifier__n_estimators": range(10, 110, 10)
    #     },
    #     {
    #         "classifier": [GradientBoostingClassifier()],
    #         "classifier__n_estimators": range(10, 110, 10),
    #         "classifier__learning_rate": np.linspace(0.1, 2.5, 20)
    #     }
    # ]

    clf = AdaBoostClassifier()

    pipeline = Pipeline([
        ('classifier', clf)
    ])

    parameters = [
        {
            "classifier__n_estimators": [10],
            "classifier__learning_rate": [1.8684210526315792]
        }
    ]

    scoring = make_scorer(f1_score)

    # Change n_jobs to -1 if you're running more than or less than 8 core cpu.
    gridSearch = GridSearchCV(pipeline,
                              parameters,
                              verbose=2,
                              n_jobs=6,
                              #                          n_jobs = -1,
                              cv=5,
                              scoring=scoring,
                              return_train_score=True)

    influnce_clf = gridSearch.fit(X_train, y_train)

    y_pred = influnce_clf.predict(X_test)

    y_train_pred = influnce_clf.predict(X_train)

    # Training error
    print(classification_report(y_true=y_train, y_pred=y_train_pred))

    print("Training Accuracy: {0}".format(accuracy_score(y_true=y_train, y_pred=y_train_pred)))

    print("Training F1 score: {0}".format(f1_score(y_true=y_train, y_pred=y_train_pred)))

    # Testing error
    print(classification_report(y_true=y_test, y_pred=y_pred))

    print("Testing Accuracy: {0}".format(accuracy_score(y_true=y_test, y_pred=y_pred)))

    print("Testing F1 score: {0}".format(f1_score(y_true=y_test, y_pred=y_pred)))

    dump(influnce_clf, 'influnce_clf.joblib')


def train_for_amount():
    wrangle = Wrangle()

    transaction = wrangle.get_transaction()

    features = transaction.columns.drop(['amount', 'influenced'])

    X = transaction[features]
    y = transaction['amount']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    numerical_columns = ['age', 'income', 'became_member_on_year', 'became_member_on_month', 'became_member_on_date',
                         'difficulty', 'duration', 'reward']

    transformer = make_union(StandardScaler())

    # This code snippet is for running all grid combination.
    #
    #
    # clf = RandomForestRegressor()
    #
    # pipeline = Pipeline([
    #     ('transformer',transformer),
    #     ('classifier',clf)
    # ])
    #
    # parameters = [
    #     {
    #         "classifier__n_estimators": range(10,110,10)
    #     },
    #     {
    #         "classifier": [AdaBoostRegressor()],
    #         "classifier__n_estimators": range(10,110,10),
    #         "classifier__learning_rate":np.linspace(0.1,2.5,20)
    #     },
    #     {
    #         "classifier": [GradientBoostingRegressor()],
    #         "classifier__n_estimators": range(10,110,10),
    #         "classifier__learning_rate":np.linspace(0.1,2.5,20)
    #     }
    # ]

    clf = GradientBoostingRegressor()

    pipeline = Pipeline([
        ('transformer', transformer),
        ('classifier', clf)
    ])

    parameters = [
        {
            "classifier__n_estimators": range(90, 130, 10),
            "classifier__learning_rate": [0.1]
        }
    ]

    scoring = make_scorer(r2_score)

    gridSearch = GridSearchCV(pipeline,
                              parameters,
                              verbose=2,
                              n_jobs=6,
                              #                          n_jobs = -1,
                              cv=5,
                              scoring=scoring,
                              return_train_score=True)

    amount_clf = gridSearch.fit(X_train, y_train)

    y_pred = amount_clf.predict(X_test)

    y_train_pred = amount_clf.predict(X_train)

    # Training error
    print(classification_report(y_true=y_train, y_pred=y_train_pred))

    print("Training R2 Score: {0}".format(r2_score(y_true=y_train, y_pred=y_train_pred)))

    print("Training MSE: {0}".format(mean_squared_error(y_true=y_train, y_pred=y_train_pred)))

    # Testing error
    print(classification_report(y_true=y_test, y_pred=y_pred))

    print("Testing R2 Score: {0}".format(r2_score(y_true=y_test, y_pred=y_pred)))

    print("Testing MSE: {0}".format(mean_squared_error(y_true=y_test, y_pred=y_pred)))

    dump(amount_clf, 'amount_clf.joblib')


def train_for_offer():
    wrangle = Wrangle()

    transaction_for_offer = consolidate_to_transaction_without_dummies(wrangle.get_transcript_clean(),
                                                                       wrangle.get_profile_for_ml(),
                                                                       wrangle.get_portfolio_for_ml())

    features = transaction_for_offer.columns.drop(
        ['difficulty', 'duration', 'bogo', 'discount', 'informational', 'email',
         'mobile', 'social', 'web', 'reward', 'offer_code'])

    X = transaction_for_offer[features]
    y = transaction_for_offer['offer_code']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # This code snippet is for running all grid combination.
    #
    # clf = RandomForestClassifier()
    #
    # pipeline = Pipeline([
    #     ('classifier',clf)
    # ])
    #
    # parameters = [
    #     {
    #         "classifier__n_estimators": range(10,110,10)
    #     },
    #     {
    #         "classifier": [AdaBoostClassifier()],
    #         "classifier__n_estimators": range(10,110,10)
    #     },
    #     {
    #         "classifier": [ExtraTreesClassifier()],
    #         "classifier__n_estimators": range(10,110,10)
    #     },
    #     {
    #         "classifier": [GradientBoostingRegressor()],
    #         "classifier__n_estimators": range(10,110,10),
    #         "classifier__learning_rate":np.linspace(0.1,2.5,20)
    #     }
    # ]

    clf = AdaBoostClassifier()

    pipeline = Pipeline([
        ('classifier', clf)
    ])

    parameters = [
        {
            "classifier": [AdaBoostClassifier()],
            "classifier__n_estimators": [10]
        }
    ]

    # Change n_jobs to -1 if you're running more than or less than 8 core cpu.
    gridSearch = GridSearchCV(pipeline,
                              parameters,
                              verbose=2,
                              n_jobs=6,
                              #                          n_jobs = -1,
                              cv=5,
                              #                          scoring=scoring,
                              return_train_score=True)

    offer_code_clf = gridSearch.fit(X_train, y_train)

    y_pred = offer_code_clf.predict(X_test)

    y_train_pred = offer_code_clf.predict(X_train)

    # Training error
    print(classification_report(y_true=y_train, y_pred=y_train_pred))

    print("Training Accuracy: {0}".format(accuracy_score(y_true=y_train, y_pred=y_train_pred)))

    print("Training F1 score: {0}".format(f1_score(y_true=y_train, y_pred=y_train_pred)))

    # Testing error
    print(classification_report(y_true=y_test, y_pred=y_pred))

    print("Testing Accuracy: {0}".format(accuracy_score(y_true=y_test, y_pred=y_pred)))

    print("Testing F1 score: {0}".format(f1_score(y_true=y_test, y_pred=y_pred)))

    dump(offer_code_clf, 'offer_code_clf.joblib')
