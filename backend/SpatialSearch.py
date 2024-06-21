import pickle as pkl
from FeatureExtraction import FeatureExtraction
import numpy as np
import heapq


class SpatialSearch:
    def __init__(self, feature_path: str):
        with open(feature_path, 'rb') as f:
            features = pkl.load(f)

        self.path_files = []
        self.vector_features = []
        self.FV = FeatureExtraction()
        for key, value in features.items():
            self.path_files.append(key)
            self.vector_features.append(value)

    def knnSearch(self, query, k):
        feature = self.FV.extract_features([query])[query]

        # Usar un heap para mantener los k vecinos más cercanos
        heap = []

        for idx, vector in enumerate(self.vector_features):
            # Calcular la distancia (por ejemplo, distancia euclidiana)
            distance = np.linalg.norm(vector - feature)

            # Si el heap tiene menos de k elementos, añadir la nueva distancia
            if len(heap) < k:
                heapq.heappush(heap, (distance, self.path_files[idx]))
            else:
                # Si el heap ya tiene k elementos, reemplazar el más lejano si el actual es más cercano
                heapq.heappushpop(heap, (distance, self.path_files[idx]))

        # Ordenar el heap por distancia
        nearest_neighbors = sorted(heap, key=lambda x: x[0])

        # Devolver solo los k vecinos más cercanos
        return [(path, dist) for dist, path in nearest_neighbors]


if __name__ == '__main__':
    search = SpatialSearch('features/features.pkl')
    res = search.knnSearch('persona.jpg', 5)

    print("Resultados de la búsqueda:")
    for r in res:
        print(r)
