"""
Chicago Crimes Dataset, Kmeans clustering
"""
from argparse import ArgumentParser, Namespace
from itertools import permutations
from typing import Iterable

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import PathCollection
from pandas.core.frame import DataFrame
from progress.spinner import Spinner
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


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
    parser.add_argument(
        "-c",
        "--clusters",
        type=int,
        required=False,
        default=3,
        help="Number of clusters to put data into",
    )

    return parser.parse_args()


def preprocessDataset(dataset: str) -> DataFrame:
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
def _visualizeClusters(
    label: np.ndarray,
    df: DataFrame,
    col1: str,
    col2: str,
    output: str,
) -> PathCollection:
    u_labels: np.ndarray = np.unique(label)
    sc: int = 0

    i: str
    for i in u_labels:
        cls = df[label == i]
        sc: PathCollection = plt.scatter(
            cls[col1], cls[col2], label="Cluster {}".format(i)
        )

    plt.legend(loc="lower left")
    plt.xlabel(col1)
    plt.ylabel(col2)
    plt.savefig(f"clusters/{output}")
    plt.clf()
    return sc


def fitKMeans(model: KMeans, labels: list, df: DataFrame, clusters: int = 3) -> KMeans:
    fitted: np.ndarray = model.fit_predict(df[labels])
    _visualizeClusters(
        label=fitted,
        df=df,
        col1=labels[0],
        col2=labels[1],
        output=f"{labels[0]}_{labels[1]}.png",
    )
    return model


def main():
    args: Namespace = parseArgs()

    df: DataFrame = preprocessDataset(args.dataset)

    perms: Iterable = permutations(df.columns.tolist(), 2)
    models: list = [KMeans(n_clusters=args.clusters) for _ in range(perms.__sizeof__())]
    modelIndex: int = 0

    with Spinner(
        f"Executing K-Means clustering with {args.clusters} clusters... "
    ) as spinner:
        for permuation in perms:
            fitKMeans(
                model=models[modelIndex],
                labels=list(permuation),
                clusters=args.clusters,
                df=df,
            )
            modelIndex += 1
            spinner.next()


if __name__ == "__main__":
    main()
