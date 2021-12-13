"""
Chicago Crimes Dataset, Kmeans clustering
"""
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


def preprocess_(data):
    df = pd.read_csv(data)
    # remove space from column names 
    df.columns = [c.lower().replace(' ', '_') for c in df.columns] 
    df = df.dropna()
    df = df.reset_index(drop=True)
    le = LabelEncoder()
    df['iucr'] = le.fit_transform(df['iucr'])
    df['primary_type'] = le.fit_transform(df['primary_type'])
    df['description'] = le.fit_transform(df['description'])
    df.replace({False: 0, True: 1}, inplace=True)
    return df

# visualize the clusters, 2d for now, and 3 clusters
def visualize_clusters(label,df, col1,col2):
    u_labels = np.unique(label) #get unique labels
    sc = 0
    
    for i in u_labels:
        cls = df[label == i]
        sc = plt.scatter(cls[col1], cls[col2], label='Cluster {}'.format(i)) #save scatter
    
    plt.legend(loc='lower left')
    
    plt.xlabel(col1)
    plt.ylabel(col2)
    
    #plt.imshow(depth_)
    output = col1 + "_" + col2
    plt.savefig(output)
    # plt.show()
    # save for later
    return sc

# labels = array of columns
def run_k_means(labels,kmeans,df):
    label = kmeans.fit_predict(df[labels])
    u_labels = np.unique(label)
    visualize_clusters(label, df, labels[0], labels[1]) # only 2d
def main():
    df = preprocess_('Crimes_-_2001_to_Present.csv')
    kmeans = KMeans(n_clusters=3, random_state=0)
    # run_k_means(['district', 'community_area'], kmeans, df)
    # run_k_means(['primary_type', 'community_area'], kmeans, df)
    run_k_means(['primary_type', 'description'], kmeans, df)

if __name__ == "__main__":
    main()
