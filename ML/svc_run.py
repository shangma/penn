from __future__ import division

import numpy as np

from merge_data import load_all

from sklearn.metrics import accuracy_score

from sklearn import svm

# def main(split=.8):


def main(len, split=.7):

    prefix = 'proc_'
    path = '../data/letter_logs/'
    X, y, label_lookup = load_all(path, len, 5, prefix=prefix)

    n, d = X.shape
    # shuffle
    idx = np.arange(n)
    np.random.shuffle(idx)
    X = X[idx]
    y = y[idx].reshape(-1)

    # split the data
    c = np.rint(split * n)

    # train on first 100 instances
    Xtrain = X[:c,:]
    ytrain = y[:c]

    # test on remaining instances
    Xtest = X[c:,:]
    ytest = y[c:]

    C = 1.
    equivalentGamma = 1.0 / (2. ** 2)
    model = svm.SVC(
        C = C,
        gamma=equivalentGamma,
        kernel='linear',
    )

    model.fit(Xtrain, ytrain)
    testPred = model.predict(Xtest)
    accuracy = accuracy_score(ytest, testPred)
    return accuracy


def svc_run(X, y, label_lookup,C=1,gamma=.0, kernel='linear', degree=3, split=.7):

    n, d = X.shape
    # shuffle
    idx = np.arange(n)
    np.random.shuffle(idx)
    X = X[idx]
    y = y[idx].reshape(-1)

    # split the data
    c = np.rint(split * n)

    # train on first 100 instances
    Xtrain = X[:c,:]
    ytrain = y[:c]

    # test on remaining instances
    Xtest = X[c:,:]
    ytest = y[c:]

    model = svm.SVC(
        C = C,
        gamma=gamma,
        kernel=kernel,
        degree=degree,
    )

    model.fit(Xtrain, ytrain)
    testPred = model.predict(Xtest)
    accuracy = accuracy_score(ytest, testPred)
    return accuracy

if __name__ == '__main__':
    split = 0.7
    prefix = 'proc_'
    path = '../data/letter_logs/'
    X, y, label_lookup = load_all(path, 5, prefix=prefix)

    n, d = X.shape
    # shuffle
    idx = np.arange(n)
    np.random.shuffle(idx)
    X = X[idx]
    y = y[idx].reshape(-1)

    # split the data
    c = np.rint(split * n)

    # train on first 100 instances
    Xtrain = X[:c,:]
    ytrain = y[:c]

    # test on remaining instances
    Xtest = X[c:,:]
    ytest = y[c:]

    C = 1.
    equivalentGamma = 1.0 / (2. ** 2)
    model = svm.SVC(
        C = C,
        gamma=equivalentGamma,
        kernel='linear',
    )

    model.fit(Xtrain, ytrain)
    testPred = model.predict(Xtest)
    accuracy = accuracy_score(ytest, testPred)
    print accuracy

    #    main()
