#!/bin/python
"""
An executable main script to classify the 2 or 3 jet dataset using the XGradient Boosted Classifier
"""
# Authors: Patrick Greenway

from sensitivity import *
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from sklearn.preprocessing import scale
from keras.models import *

variables_map = {
    2: ['mBB', 'dRBB', 'pTB1', 'pTB2', 'MET', 'dPhiVBB','dPhiLBmin', 'Mtop', 'dYWH', 'mTW', 'pTV'],
    3: ['mBB', 'dRBB', 'pTB1', 'pTB2', 'MET', 'dPhiVBB','dPhiLBmin', 'Mtop', 'dYWH', 'mTW', 'pTV', 'mBBJ', 'pTJ3']
        }

nJets = 2
variables = variables_map[nJets]

def main():
    print "MVA analysis on the " + str(nJets) + " Jet Dataset"
    #Get prepared data frames ready to be inserted into classifier
    df_even = pd.read_csv('../CSV_Results_v7/allVariables_'+str(nJets)+'jet_even.csv', index_col=0)
    df_odd = pd.read_csv('../CSV_Results_v7/allVariables_'+str(nJets)+'jet_odd.csv', index_col=0)
    
    print "Data frames loaded."
    
    df_even[variables] = scale(df_even[variables])
    df_odd[variables] = scale(df_odd[variables])
    
    print "Training Classifier..."
    clf_even = Sequential()
    clf_even.add(Dense(14, activation="relu", kernel_initializer='uniform', input_dim=len(variables)))
    clf_even.add(Dense(14, activation="relu", kernel_initializer="uniform"))
    clf_even.add(Dense(14, activation="relu", kernel_initializer="uniform"))
    clf_even.add(Dense(1, activation="sigmoid", kernel_initializer="uniform"))
    clf_even.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    clf_odd = Sequential()
    clf_odd.add(Dense(14, activation="relu", kernel_initializer='uniform', input_dim=len(variables)))
    clf_odd.add(Dense(14, activation="relu", kernel_initializer="uniform"))
    clf_odd.add(Dense(14, activation="relu", kernel_initializer="uniform"))
    clf_odd.add(Dense(1, activation="sigmoid", kernel_initializer="uniform"))
    clf_odd.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    clf_even.fit(df_even[variables], df_even['Class'], sample_weight=df_even['training_weight'], epochs=5, batch_size=32)
    
    clf_odd.fit(df_odd[variables], df_odd['Class'], sample_weight=df_odd['training_weight'], epochs=5, batch_size=32)
    
    print "Testing Classifier..."
    scores_even = clf_odd.predict_proba(df_even[variables])[:,0]
    scores_odd = clf_even.predict_proba(df_odd[variables])[:,0]
    df_even['decision_value'] = ((scores_even-0.5)*2)
    df_odd['decision_value'] = ((scores_odd-0.5)*2)
    df = df_even.append(df_odd)
    
    # TrafoD and score sensitivity.
    sensitivity, error = calc_sensitivity_with_error(df)
    print "Sensitivity for  " + str(nJets) + " Jet Dataset is: {:f}".format(sensitivity) + " +/- {:f}".format(error)

    #Plot BDT.
    print "Plotting histogram..."
    #decision_plot(df, show=True, block=True)
    print "Script finished."

if __name__ == '__main__':
    main()
    
