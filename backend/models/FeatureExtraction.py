import tensorflow as tf
from tensorflow.keras.applications import InceptionV3  # type: ignore
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.applications.inception_v3 import preprocess_input  # type: ignore
import numpy as np
import pickle as pkl
from tqdm import tqdm


class FeatureExtraction:
    def __init__(self):
        self.model = InceptionV3(
            weights='imagenet', include_top=False, pooling='avg')
        print("Model loaded successfully")

    def __load_and_preprocess_image(self, img_path):
        img = image.load_img(img_path, target_size=(299, 299))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        return preprocess_input(img_array)

    def extract_features(self, img_paths: list):
        if img_paths is None or len(img_paths) == 0:
            raise ValueError(
                "img_paths must be a non-empty list of image paths")

        features = []
        features_dict = {}

        for img_path in tqdm(img_paths, desc="Processing images"):
            img = self.__load_and_preprocess_image(img_path)
            f = self.model.predict(img, verbose=0)
            features.append(f.flatten())

        features = np.array(features)

        # norma l2

        features = features / np.linalg.norm(features, axis=1)[:, None]

        for i, img_path in enumerate(img_paths):
            features_dict[img_path] = features[i]

        return features_dict

    def extract_one_feature(self, img_path: str):
        img = self.__load_and_preprocess_image(img_path)
        f = self.model.predict(img, verbose=0)
        f = f.flatten()
        f = f / np.linalg.norm(f)
        return f

    def save_features(self, features_dict, save_path):
        print(f"Saving features to {save_path}. Please wait...")
        with open(save_path, 'wb') as f:
            pkl.dump(features_dict, f)
