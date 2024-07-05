from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.SpatialSearch import SpatialSearch
import time
import os
import base64

app = FastAPI()
spatial = None

TEMPORARY_FOLDER = "temp/"

if not os.path.exists(TEMPORARY_FOLDER):
    os.makedirs(TEMPORARY_FOLDER)

origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create_index")
def create_index():
    global spatial
    if spatial is None:
        spatial = SpatialSearch('features/features.pkl',
                                'features/rtree', 'features/faiss.index')
        return {"message": "Index created successfully", "status_code": 200}
    else:
        return HTTPException(status_code=400, detail="Index already created")


@app.post("/search")
async def upload_file(image: UploadFile = File(...), type_search: str = Form(...), k: float = Form(...)):

    if spatial is None:
        return HTTPException(status_code=400, detail="Index not created")

    if image.content_type != "image/jpeg" and image.content_type != "image/png" and image.content_type != "image/jpg" and image.content_type != "image/webp":
        return HTTPException(status_code=400, detail="Invalid image format")

    file_location = os.path.join(TEMPORARY_FOLDER, image.filename)
    with open(file_location, "wb") as f:
        f.write(await image.read())

    start = time.time()
    if type_search == "sequential":
        res = spatial.knn_sequential(file_location, int(k))
    elif type_search == "range":
        res = spatial.range_search(file_location, float(k))
    elif type_search == "rtree":
        res = spatial.rtree_knn_search(file_location, int(k))
    elif type_search == "faiss":
        res = spatial.faiss_knn_search(file_location, int(k))
    else:
        return HTTPException(status_code=400, detail="Invalid search type")

    end = time.time()

    os.remove(file_location)

    results = []

    for r in res:
        image_path, distance_value = r
        image_path = image_path.replace("\\", "/")
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
        # Convertir time_value a float
        results.append(
            {"image": encoded_string, "distance": float(distance_value)})

    return {"message": "Search completed successfully", "status_code": 200, "time": end-start, "results": results}
