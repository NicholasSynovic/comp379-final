import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
df.columns = [c.lower().replace(' ', '_') for c in df.columns]
df = df.dropna()
df = df.reset_index(drop=True)
df = df.drop(['date', 'latitude', 'longitude', 'location'], axis = 1)

le = LabelEncoder()
df['iucr'] = le.fit_transform(df['iucr'])
df['primary_type'] = le.fit_transform(df['primary_type'])
df['description'] = le.fit_transform(df['description'])
df['location_description'] = le.fit_transform(df['location_description'])
df['fbi_code'] = le.fit_transform(df['fbi_code'])

y_train = df['arrest']
X_train = df.drop('arrest', axis = 1)
feat_labels = X_train.columns

forest = RandomForestClassifier(n_estimators = 500, random_state = 1)
forest.fit(X_train, y_train)

importances = forest.feature_importances_

indices = np.argsort(importances)[::-1]

for f in range(X_train.shape[1]):
    print("%2d) %-*s %f" % (f + 1, 30,
                            feat_labels[indices[f]],
                            importances[indices[f]]))

plt.title('Feature Importance')
plt.bar(range(X_train.shape[1]),
        importances[indices],
        align = 'center')

for i in range(X_train.shape[1]):
    plt.text(i, round(importances[indices[i]], 3), round(importances[indices[i]], 3), ha = 'center')

plt.xticks(range(X_train.shape[1]),
            feat_labels[indices], rotation = 90)
plt.xlim([-1, X_train.shape[1]])

plt.xlabel('Features')
plt.ylabel('Importance Score')

plt.tight_layout()
plt.show()