from models.SpatialSearch import SpatialSearch

if __name__ == '__main__':
    # Inicializa la búsqueda espacial con el archivo de características guardado
    search = SpatialSearch('features/features.pkl',
                           'features/rtree', 'features/faiss.index')

    res = search.knn_sequential('images/9964.jpg', 10)

    print("Resultados de la búsqueda secuencial:")
    for r in res:
        print(r)

    res = search.range_search('images/9964.jpg', 0.3)

    print("Resultados de la búsqueda por rango:")
    for r in res:
        print(r)

    res = search.rtree_knn_search('images/9964.jpg', 10)

    print("Resultados de la búsqueda con R-Tree:")
    for r in res:
        print(r)

    res = search.faiss_knn_search('images/9964.jpg', 10)

    print("Resultados de la búsqueda con Faiss:")
    for r in res:
        print(r)
