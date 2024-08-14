"""
library

import piplite
await piplite.install(['numpy'])
await piplite.install(['pandas'])
await piplite.install(['seaborn'])
"""

# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
import pandas as pd
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier


#useful
#confusion matrix function
def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 



#fetch file
from js import fetch
import io

URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
resp1 = await fetch(URL1)
text1 = io.BytesIO((await resp1.arrayBuffer()).to_py())
data = pd.read_csv(text1)

URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
resp2 = await fetch(URL2)
text2 = io.BytesIO((await resp2.arrayBuffer()).to_py())
X = pd.read_csv(text2)


#convert 'Class' to numpy array (better analyse)
Y = data['Class'].to_numpy()
#create StandardScaler() object and assign to 'transform'
#removing mean and scaling to unit variance (mean: 0, standard deviation: 1)
transform = preprocessing.StandardScaler() 
X = transform.fit_transform(X)
#train test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
#check number of samples (split correct or not)
Y_test.shape



#after we got test and train data:
#logistic regression
parameters ={"C":[0.01,0.1,1],'penalty':['l2'], 'solver':['lbfgs']}# l1 lasso l2 ridge
lr=LogisticRegression()
# Initialize GridSearchCV
logreg_cv = GridSearchCV(estimator=lr, 
                           param_grid=parameters, 
                           cv=10)
# Fit the model
logreg_cv.fit(X_train, Y_train)
# see result
print("tuned hpyerparameters :(best parameters) ",logreg_cv.best_params_)
print("accuracy :",logreg_cv.best_score_) #expected average performance (use training data and cross validation)

#we use model with best paramters
best_lr = logreg_cv.best_estimator_
#see best model result:
from sklearn.metrics import accuracy_score
Y_pred = best_lr.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred) #better to mimic real world (use unseen data, Y_test)
print("Test Set Accuracy:", accuracy)
#confusion matrix:
yhat=logreg_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)
"""
Y_pred = best_lr.predict(X_test)
accuracy = accuracy_score(Y_test, Y_pred)

and

accuracy = best_lr.score(X_test,Y_test)

are the same
"""


#support vector machine
parameters_svm = {'kernel':('linear', 'rbf','poly','rbf', 'sigmoid'),
              'C': np.logspace(-3, 3, 5),
              'gamma':np.logspace(-3, 3, 5)}
svm = SVC()
svm_cv = GridSearchCV(estimator=svm, 
                        param_grid = parameters_svm, 
                        scoring='accuracy', 
                        cv=10)
# Fit the model
svm_cv.fit(X_train, Y_train)
#see result
print("tuned hpyerparameters :(best parameters) ",svm_cv.best_params_)
print("accuracy :",svm_cv.best_score_)

#use model with best parameters
best_svm = svm_cv.best_estimator_
Y_pred = best_svm.predict(X_test)
accuracy_svm = accuracy_score(Y_test, Y_pred)
print("Test Set Accuracy:", accuracy_svm)
#confusion matrix
yhat=svm_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)








#decision tree classifier
parameters_tree = {'criterion': ['gini', 'entropy'],
     'splitter': ['best', 'random'],
     'max_depth': [2*n for n in range(1,10)],
     'max_features': ['auto', 'sqrt'],
     'min_samples_leaf': [1, 2, 4],
     'min_samples_split': [2, 5, 10]}

tree = DecisionTreeClassifier()
tree_cv = GridSearchCV(estimator=tree, 
                        param_grid = parameters_tree, 
                        scoring='accuracy', 
                        cv=10)
# Fit the model
tree_cv.fit(X_train, Y_train)
#result
print("tuned hpyerparameters :(best parameters) ",tree_cv.best_params_)
print("accuracy :",tree_cv.best_score_)
#best model
tree_best = tree_cv.best_estimator_
accuracy = tree_best.score(X_test, Y_test)
print("Test Set Accuracy:", accuracy)
#confusion matrix
yhat = tree_cv.predict(X_test)
plot_confusion_matrix(Y_test,yhat)





#k nearest neighbor (KNN)
parameters_knn = {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
              'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
              'p': [1,2]}

KNN = KNeighborsClassifier()
knn_cv = GridSearchCV(estimator=KNN, 
                        param_grid = parameters_knn, 
                        scoring='accuracy', 
                        cv=10)
# Fit the model
knn_cv.fit(X_train, Y_train)
###############################
#the rest result, best model and confusion matrix are the same


"""
SVM paramters(kernel):

1. Linear (when problem is simple)
2. RBF (non-linear, when dont have prior knowledge about the data; most commonly used kernel in practice)
3. sigmod (less common, use when resembel ANN)
"""
