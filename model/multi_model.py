
## this discussion could be useful==> https://www.kaggle.com/serigne/stacked-regressions-top-4-on-leaderboard

def multi_model(zipcode):

    import math
    import csv
    import numpy as np
    import json
    from flask import jsonify
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import ShuffleSplit
    from sklearn.model_selection import cross_val_predict
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import Ridge
    from sklearn.externals import joblib
    from sklearn.neural_network import MLPRegressor
    from sklearn.ensemble import GradientBoostingRegressor



    #n_dim is the number of feature
    n_dim=2;
    data_X = np.empty(shape=[0, n_dim])
    data_Y = np.empty(shape=[0, 1])
    #print(train_X)
    #print(train_Y)


    # In[45]:

    with open('data/House_Zipcode_LL.csv', 'r') as csvfile:
        csvReader = csv.reader(csvfile)
        legend = next(csvReader)
        for row in csvReader:
            x_cur = []
            x_cur.append(float(row[legend.index("lat")]))
            x_cur.append(float(row[legend.index("long")]))
            data_X = np.vstack((data_X, x_cur))
            data_Y = np.vstack((data_Y,float(row[legend.index("2017-09")])))
    data_Y=np.ravel(data_Y)

    with open('data/Zipcode_LL.csv', 'r') as zipcodell:
        csvReader = csv.reader(zipcodell)
        legend = next(csvReader)
        for row in csvReader:
            if(int(row[legend.index("Zipcode")]) == zipcode):
                test_Lat = float(row[legend.index("lat")])
                test_Long = float(row[legend.index("long")])
                break

    #this line is to manually split the data to train and test, 
    #for real fitting, use cross-validation to test the model and parameter, use the whole data for training
    # change test_size to 0 to use all the data for training
    X_train, X_test, Y_train, Y_test = train_test_split(
        data_X, data_Y, test_size=0.05, random_state=0)


    #random forest regressor

    rf_model = RandomForestRegressor(n_estimators=20, criterion='mse',                                 max_depth=None, min_samples_split=2, min_samples_leaf=1,                                  min_weight_fraction_leaf=0.0, max_features='auto',                                  max_leaf_nodes=None, min_impurity_decrease=0.0,                                  min_impurity_split=None, bootstrap=True, oob_score=False,                                  n_jobs=1, random_state=None, verbose=0, warm_start=False)

    cv_para = ShuffleSplit(n_splits=3, test_size=0.1, random_state=1)
    print ('cross validation score of rf_model: '+str(cross_val_score(rf_model, X_train, Y_train, cv=cv_para, scoring='r2').mean()))

    rf_model.fit(X_train, Y_train)
    print ('rf test score= '+str(rf_model.score(X_test, Y_test)))
    print ('rf train score= '+str(rf_model.score(X_train, Y_train)))


    #example to predict price of certain [lat,long] location
    rf_prediction = rf_model.predict([[test_Lat, test_Long]])
    return json.dumps(rf_prediction.tolist())

    # save the trained model to file, so that there is no need to retrain the data
    joblib.dump(rf_model, 'rf_model.pkl')
    #to use saved model to predict, this saved model can also be used in another python code
    rf_model_2 = joblib.load('rf_model.pkl')
    #rf_model_2.predict([[34.034515,-84.707349]])

    print ('train size= '+str(Y_train.size)+', test size= '+str(Y_test.size))



    ridge_model = Ridge(alpha=0.1, fit_intercept=True, normalize=False, copy_X=True, 
          max_iter=None, tol=0.001, solver='auto', random_state=None)
    print ('cross validation score of Ridge_model: '+ str(cross_val_score(ridge_model, X_train, Y_train,                     cv=cv_para, scoring='r2').mean()))
    ridge_model.fit(X_train, Y_train)

    print ('ridge test score= '+str(rf_model.score(X_test, Y_test)))
    print ('ridge train score= '+str(rf_model.score(X_train, Y_train)))

    #example to predict price of certain [lat,long] location
    ridge_model.predict([[34.034515,-84.707349]])



    joblib.dump(ridge_model, 'ridge_model.pkl')
    #to use saved model to predict
    ridge_model_2 = joblib.load('ridge_model.pkl')


    # Neural network model

    #ref of varying regularization parameters:  http://scikit-learn.org/stable/auto_examples/neural_networks/plot_mlp_alpha.html#sphx-glr-auto-examples-neural-networks-plot-mlp-alpha-py
    nn_model = MLPRegressor(hidden_layer_sizes=(20, ), activation='relu',
                 solver='adam', alpha=0.00001, batch_size='auto',
                 learning_rate='constant', learning_rate_init=0.001,
                 power_t=0.5, max_iter=500, shuffle=True,
                 random_state=None, tol=0.001, verbose=False, 
                 warm_start=False, momentum=0.9, nesterovs_momentum=True, 
                 early_stopping=False, validation_fraction=0.1,
                 beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    print ('cross validation score of nn_model: '+ str(cross_val_score(nn_model, X_train, Y_train,                     cv=cv_para, scoring='r2').mean()))

    nn_model.fit(X_train, Y_train)

    print ('nn test score= '+str(nn_model.score(X_test, Y_test)))
    print ('nn train score= '+str(nn_model.score(X_train, Y_train)))


    joblib.dump(nn_model, 'nn_model.pkl')
    #to use saved model to predict
    nn_model_2 = joblib.load('nn_model.pkl')
    nn_model.predict([[34.034515,-84.707349]])



    ##GradientBoostingRegressor
    GBR_model = GradientBoostingRegressor(loss = 'ls',n_estimators=20, max_depth = 5,
                                         min_samples_split = 2, learning_rate = 0.1)
    print ('cross validation score of GBR_model: '+ str(cross_val_score(GBR_model, X_train, Y_train, cv=cv_para, scoring='r2').mean()))

    GBR_model.fit(X_train, Y_train)

    print ('GBR test score= '+str(GBR_model.score(X_test, Y_test)))
    print ('GBR train score= '+str(GBR_model.score(X_train, Y_train)))


    joblib.dump(GBR_model, 'GBR_model.pkl')
    #to use saved model to predict
    GBR_model_2 = joblib.load('GBR_model.pkl')
    GBR_model.predict([[34.034515,-84.707349]])

