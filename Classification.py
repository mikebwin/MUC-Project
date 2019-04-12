import pandas as pd
from math import sqrt
from matplotlib import pyplot
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

data = pd.read_csv("data.csv", index_col=False)

X = data.loc[:, 'Light' : 'Sound']
y = data.loc[:, 'Engagement']


X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.3, random_state=42)    

knn = KNeighborsClassifier(5)
classifiers = [SVC(gamma=2, C=1), knn, MLPClassifier(alpha=1)]

for clf in classifiers:
    clf.fit(X_train, y_train)
    score = clf.score(X_test, y_test)
    
    print(score)
    
#knn.fit(X_train, y_train)
#prediction = knn.predict(X_test)
#print(metrics.accuracy_score(y_test, prediction))