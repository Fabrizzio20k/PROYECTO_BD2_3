import pickle as pkl
from models.FeatureExtraction import FeatureExtraction
import numpy as np
import heapq
from rtree import index
import os
from tqdm import tqdm
from sklearn.decomposition import PCA
import faiss


class SpatialSearch:
    def __init__(self, feature_path: str, r_tree_path: str, faiss_path: str):
        # Carga las características desde el archivo pickle
        with open(feature_path, 'rb') as f:
            features = pkl.load(f)

        self.path_files = []
        self.vector_features = []
        self.FV = FeatureExtraction()
        for key, value in features.items():
            self.path_files.append(key)
            self.vector_features.append(value)

        self.__pca = PCA(n_components=100)
        self.__rtree_vector_features = self.__pca.fit_transform(
            self.vector_features)

        # Carga el índice R-Tree
        self.__p = index.Property()
        self.__p.dimension = 100
        self.__p.filename = r_tree_path

        # Si el archivo del índice R-Tree no existe, se crea uno nuevo
        if not os.path.exists(r_tree_path + '.dat') or not os.path.exists(r_tree_path + '.idx'):
            self.__idx = index.Index(r_tree_path, properties=self.__p)
            for idx, vector in tqdm(enumerate(self.__rtree_vector_features), total=len(self.__rtree_vector_features)):
                self.__idx.insert(idx, vector)
            print("R-Tree index created successfully.")

        # Si el archivo del índice R-Tree ya existe, se carga
        else:
            self.__idx = index.Index(r_tree_path, properties=self.__p)
            print("R-Tree index loaded successfully.")

        # Carga el índice de búsqueda de Faiss
        self.__faiss_index = faiss.IndexFlatL2(2048)

        # Si el archivo del índice de Faiss no existe, se crea uno nuevo
        if not os.path.exists(faiss_path):
            self.__faiss_index.add(np.array(self.vector_features))
            faiss.write_index(self.__faiss_index, faiss_path)
            print("Faiss index created successfully.")

        # Si el archivo del índice de Faiss ya existe, se carga
        else:
            self.__faiss_index = faiss.read_index(
                faiss_path, faiss.IO_FLAG_MMAP)
            print("Faiss index loaded successfully.")

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

    def rtree_knn_search(self, query, k):
        feature = self.FV.extract_one_feature(query)
        feature = self.__pca.transform([feature])[0]

        k_nearest = list(self.__idx.nearest(feature, num_results=k))

        results = []
        for idx in k_nearest:
            distance = np.linalg.norm(self.__rtree_vector_features[idx] - feature)
            results.append((distance, self.path_files[idx]))

        results.sort(key=lambda x: x[0])

        return [(path, dist) for dist, path in results]

    def faiss_knn_search(self, query, k):

        feature = self.FV.extract_one_feature(query)
        distances, indices = self.__faiss_index.search(np.array([feature]), k)
        return [(self.path_files[idx], dist) for dist, idx in zip(distances[0], indices[0])]
