import pickle as pkl
from FeatureExtraction import FeatureExtraction
import numpy as np
import heapq
from rtree import index
import os
from tqdm import tqdm


class SpatialSearch:
    def __init__(self, feature_path: str, r_tree_path: str):
        # Carga las características desde el archivo pickle
        with open(feature_path, 'rb') as f:
            features = pkl.load(f)

        self.path_files = []
        self.vector_features = []
        self.FV = FeatureExtraction()
        for key, value in features.items():
            self.path_files.append(key)
            self.vector_features.append(value)

    def knn_sequential(self, query, k):
        feature = self.FV.extract_one_feature(query)
        heap = []

        for idx, vector in enumerate(self.vector_features):
            distance = np.linalg.norm(vector - feature)
            if len(heap) < k:
                heapq.heappush(heap, (-distance, self.path_files[idx]))
            else:
                heapq.heappushpop(heap, (-distance, self.path_files[idx]))

        nearest_neighbors = sorted(heap, key=lambda x: x[0], reverse=True)
        return [(path, -dist) for dist, path in nearest_neighbors]

    def range_search(self, query, radius):
        feature = self.FV.extract_one_feature(query)
        results = []

        for idx, vector in enumerate(self.vector_features):
            distance = np.linalg.norm(vector - feature)
            if distance <= radius:
                results.append((self.path_files[idx], distance))

        results = sorted(results, key=lambda x: x[1])
        return results


if __name__ == '__main__':
    # Inicializa la búsqueda espacial con el archivo de características guardado
    search = SpatialSearch('features/features.pkl', 'features/rtree.idx')

    res = search.knn_sequential('images/9964.jpg', 10)

    print("Resultados de la búsqueda secuencial:")
    for r in res:
        print(r)

    res = search.range_search('images/9964.jpg', 0.3)

    print("Resultados de la búsqueda por rango:")
    for r in res:
        print(r)
