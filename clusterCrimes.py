"""
Chicago Crimes Dataset, Kmeans clustering
"""
from matplotlib.collections import PathCollection
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.core.frame import DataFrame
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

from argparse import ArgumentParser, Namespace


def parseArgs() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog="Cluster Crimes",
        usage="Execute K-Means clustering on a Chicago Crimes Dataset",
        description="Datasets can be downloaded from: https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data",
    )
    parser.add_argument(
        "-d",
        "--dataset",
        type=str,
        required=True,
        help="Dataset filename",
        )
    parser.add_argument("-o",
        "--output",
        type=str,
        required=True,
        help="Output filename",
        )
    return parser.parse_args()


def preprocessDataset(dataset:str)    -> DataFrame:
    df: DataFrame = pd.read_csv(dataset)
    # remove space from column names
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df = df.dropna()
    df = df.reset_index(drop=True)
    le: LabelEncoder = LabelEncoder()
    df["iucr"] = le.fit_transform(df["iucr"])
    df["primary_type"] = le.fit_transform(df["primary_type"])
    df["description"] = le.fit_transform(df["description"])
    df.replace({False: 0, True: 1}, inplace=True)
    return df


# visualize the clusters, 2d for now, and 3 clusters
def _visualizeClusters(label, df, col1, col2, output:str) -> PathCollection:
    u_labels: np.ndarray = np.unique(label)  # get unique labels
    sc:int = 0

    i: str
    for i in u_labels:
        cls = df[label == i]
        sc: PathCollection = plt.scatter(
            cls[col1], cls[col2], label="Cluster {}".format(i)
        )  # save scatter

    plt.legend(loc="lower left")

    plt.xlabel(col1)
    plt.ylabel(col2)

    # plt.imshow(depth_)
    plt.savefig(output)
    # plt.show()
    # save for later
    return sc


# labels = array of columns
def fitKMeans(labels, kmeans, df):
    label = kmeans.fit_predict(df[labels])
    u_labels = np.unique(label)
    _visualizeClusters(label, df, labels[0], labels[1], output="output.png")  # only 2d


def main():
    args: Namespace = parseArgs()

    df: DataFrame = preprocessDataset(args.dataset)

    kmeans:KMeans = KMeans(n_clusters=3, random_state=0)

    # run_k_means(['district', 'community_area'], kmeans, df)
    # run_k_means(['primary_type', 'community_area'], kmeans, df)
    fitKMeans(["primary_type", "description"], kmeans, df)


if __name__ == "__main__":
    main()
