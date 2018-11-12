import tensorflow as tf
import math
import csv
import numpy as np
from flask import jsonify

def lr_model(zipcode):

    train_Long = np.array([0])
    train_Lat = np.array([0])
    train_Y = np.array([0])

    center_Lat = 33.7537
    center_Long = -84.3863

    steps = 100
    learn_rate = 0.0001

    # Model linear regression y = Wx + b
    x = tf.placeholder(tf.float32, [None, 1])
    W = tf.Variable(tf.zeros([1,1]))
    b = tf.Variable(tf.zeros([1]))
    product = tf.matmul(x,W)
    y = product + b
    y_ = tf.placeholder(tf.float32, [None, 1])

    # Cost function sum((y_-y)**2)
    cost = tf.reduce_mean(tf.square(y_-y))

    # Training using Gradient Descent to minimize cost
    train_step = tf.train.GradientDescentOptimizer(learn_rate).minimize(cost)

    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)

    all_points = [];
    eq_vals = [];

    with open('data/House_Zipcode_LL.csv', 'r') as csvfile:
        csvReader = csv.reader(csvfile)
        legend = next(csvReader)
        for row in csvReader:
            temp1 = []
            temp2 = []
            temp1.append(float(row[legend.index("lat")]))
            train_Lat = np.vstack((train_Lat, temp1))
            temp2.append(float(row[legend.index("long")]))
            train_Long = np.vstack((train_Long, temp2))
            train_Y = np.vstack((train_Y,float(row[legend.index("2017-09")])))


    with open('data/Zipcode_LL.csv', 'r') as zipcodell:
        csvReader = csv.reader(zipcodell)
        legend = next(csvReader)
        for row in csvReader:
            if(int(row[legend.index("Zipcode")]) == zipcode):
                test_Lat = float(row[legend.index("lat")])
                test_Long = float(row[legend.index("long")])
                break

    for i in range(1, train_Y.size):
        # Create fake data for y = W.x + b where W = 2, b = 0
        distance = math.sqrt((train_Lat[i] - center_Lat)**2+ (train_Long[i] - center_Long)**2)
        xs = np.array([[distance]])
        ys = np.array([train_Y[i]])
        type(xs)
        # Train
        feed = { x: xs, y_: ys }
        sess.run(train_step, feed_dict=feed)
        
        all_points.append({"x": xs, "y": ys});

        # NOTE: W should be close to 2, and b should be close to 0 

    eq_vals.append({'w': str(sess.run(W)[0][0]), "b": str(sess.run(b)[0]), 
                "cost": '{0:f}'.format(sess.run(cost, feed_dict=feed))});
    test_distance = math.sqrt((test_Lat - center_Lat)**2+ (test_Long - center_Long)**2)
    xt = np.array([[test_distance]])
    #test_price = sess.run(y_,feed_dict = {x : xt})
    print(type(eq_vals[0]['w']))
    print(eq_vals[0]['w'])
    test_price = float(eq_vals[0]['w']) * test_distance + float(eq_vals[0]['b'])

    eq_vals.append({'test_price': str(test_price)})
    #response = jsonify(results=[eq_vals])
    #response = jsonify(results = [eq_vals])
    return eq_vals