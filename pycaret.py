# -*- coding: utf-8 -*-
"""Pycaret.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KHifvTNzfEg-WuVf6gOklNTwVcVwRPec
"""

pip install pycaret

pip install pycaret[full]

#from google.colab import drive
#drive.mount('/content/drive')
#drive.mount('/content/gdrive', force_remount=True)
#root_path = 'gdrive/My Drive/Classeur1 (1).xlsx'

import pandas as pd

from google.colab import drive
drive.mount('/content/drive')

Dataset=pd.read_excel('/content/drive/MyDrive/SYLOS.xlsx')
Dataset.head(10)

Dataset.ffill(inplace=True)
Dataset.head(10)

Dataset.shape

Dataset.describe()

# sample 5% of data to be used as unseen data
data = Dataset.sample(frac=0.95, random_state=786)
data_unseen = Dataset.drop(data.index)
data.reset_index(inplace=True, drop=True)
data_unseen.reset_index(inplace=True, drop=True)
# print the revised shape
print('Data for Modeling: ' + str(data.shape))
print('Unseen Data For Predictions: ' + str(data_unseen.shape))

import numpy as np

# init setup
from pycaret.classification import *
s = setup(data = data, target = 'classification', session_id=123)

best_model = compare_models()

from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.ensemble import RandomForestClassifier

print(best_model)
#>>> OUTPUT
RidgeClassifier(alpha=1.0, class_weight=None, copy_X=True, fit_intercept=True,
                max_iter=None, normalize=False, random_state=123, solver='auto',
                tol=0.001)

# check available models
models()

import warnings
import numpy as np

with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)
    print('x' in np.arange(2))   #returns False, warning is suppressed

print('x' in np.arange(10))   #returns False, Throws FutureWarning

dt = create_model('dt')

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# trained model object is stored in the variable 'dt'. 
print(dt)
#>>> OUTPUT
DecisionTreeClassifier(ccp_alpha=0.0, class_weight=None, criterion='gini',
                       max_depth=None, max_features=None, max_leaf_nodes=None,
                       min_impurity_decrease=0.0, min_impurity_split=None,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, presort='deprecated',
                       random_state=123, splitter='best')

knn = create_model('knn')

svm = create_model('svm')

rf = create_model('rf')

tuned_dt = tune_model(dt)

# tuned model object is stored in the variable 'tuned_dt'. 
print(tuned_dt)
#>>> OUTPUT
DecisionTreeClassifier(ccp_alpha=0.0, class_weight=None, criterion='entropy',
                       max_depth=6, max_features=1.0, max_leaf_nodes=None,
                       min_impurity_decrease=0.002, min_impurity_split=None,
                       min_samples_leaf=5, min_samples_split=5,
                       min_weight_fraction_leaf=0.0, presort='deprecated',
                       random_state=123, splitter='best')

tuned_dt = tune_model(dt)

tuned_svm = tune_model(svm)

import numpy as np
tuned_knn = tune_model(knn, custom_grid = {'n_neighbors' : np.arange(0,50,1)})

print(tuned_knn)
#OUTPUT
KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                     metric_params=None, n_jobs=-1, n_neighbors=42, p=2,
                     weights='uniform')

tuned_rf = tune_model(rf, optimize='Accuracy')

predict_model(tuned_rf)

pip install matplotlib==3.1.3

plot_model(tuned_rf, plot = 'auc')

plot_model(tuned_rf, plot = 'pr')

plot_model(tuned_rf, plot='feature')

#plt.figure(figsize = (18,9))
import matplotlib.pyplot as plt
plot_model(tuned_rf, plot='feature')
plt.savefig('/content/drive/MyDrive/results_features_important.svg')

plot_model(tuned_rf, plot = 'confusion_matrix')

evaluate_model(tuned_rf)

predict_model(tuned_rf);

# finalize rf model
final_rf = finalize_model(tuned_rf)
# print final model parameters
print(final_rf)
#>>> OUTPUT
RandomForestClassifier(bootstrap=False, ccp_alpha=0.0, class_weight={},
                       criterion='entropy', max_depth=5, max_features=1.0,
                       max_leaf_nodes=None, max_samples=None,
                       min_impurity_decrease=0.0002, min_impurity_split=None,
                       min_samples_leaf=5, min_samples_split=10,
                       min_weight_fraction_leaf=0.0, n_estimators=150,
                       n_jobs=-1, oob_score=False, random_state=123, verbose=0,
                       warm_start=False)

predict_model(final_rf);

unseen_predictions = predict_model(final_rf, data=data_unseen)
unseen_predictions.head(10)

unseen_predictions.to_csv('/content/drive/MyDrive/results_class_sylos.csv', index=False)

# check metric on unseen data
from pycaret.utils import check_metric
check_metric(unseen_predictions['classification'], unseen_predictions['Label'], metric = 'Accuracy')
#>>> OUTPUT

# saving the final model
save_model(final_rf,'Final RF Model 11Nov2020')

# loading the saved model
saved_final_rf = load_model('Final RF Model 11Nov2020')

# predict on new data
new_prediction = predict_model(saved_final_rf, data=data_unseen)
new_prediction.head(10)

from pycaret.utils import check_metric
check_metric(new_prediction['classification'], new_prediction['Label'], metric = 'Accuracy')

