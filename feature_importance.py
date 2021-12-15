import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

df = pd.read_csv("Processed Dataset.csv")

y_train = df['Arrest']
X_train = df.drop('Arrest', axis = 1)
feat_labels = X_train.columns

forest = RandomForestClassifier(n_estimators = 500, random_state = 1)
forest.fit(X_train, y_train)

importances = forest.feature_importances_

indices = np.argsort(importances)[::-1]

for f in range(X_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30,
                            feat_labels[indices[f]],
                            importances[indices[f]]))

plt.bar(range(X_train.shape[1]),
        importances[indices],
        align = 'center')

for i in range(X_train.shape[1]):
    plt.text(i, round(importances[indices[i]], 3), round(importances[indices[i]], 3), ha = 'center')

plt.xticks(range(X_train.shape[1]),
            feat_labels[indices], rotation = 90)
plt.xlim([-1, X_train.shape[1]])

plt.title('Feature Importances for \'Arrest\' Prediction')
plt.xlabel('Features')
plt.ylabel('Importance Score')

plt.tight_layout()
plt.show()