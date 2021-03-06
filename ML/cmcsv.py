import csv
import numpy as np
from sklearn.metrics import confusion_matrix

# Debugging
import matplotlib.pyplot as plt

'''
INPUT:
    y_pred: length n numpy array of predicted label
    y_true: length n numpy array of true label

RETURNS:
    cm_norm: normalized confusion matrix
'''
def cmcsv(f_name, y_pred, y_true, label_lookup):
    cm = confusion_matrix(y_pred, y_true)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    with open(f_name+'.csv','w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['label'] + label_lookup.values())
        for ii in xrange(cm.shape[0]):
            writer.writerow([label_lookup[ii]] + ['%.1f' % (x*100) for x in cm_norm[ii,:]])

    # Debugging
    '''
    plt.matshow(cm_norm)
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.colorbar()
    plt.show()
    '''



def cmplt(f_name, y_pred, y_true, label_lookup):
    cm = confusion_matrix(y_pred, y_true)
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.clf()
    plt.matshow(cm_norm)
    plt.xlabel('Predicted label')
    plt.ylabel('True label')
    plt.colorbar()
    # plt.show()
    plt.savefig(f_name)


