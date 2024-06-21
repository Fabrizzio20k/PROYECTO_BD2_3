import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle as pkl
from tqdm import tqdm


class FeatureExtraction:
    def __init__(self):
        base_model = InceptionV3(weights='imagenet', include_top=False)
        x = base_model.output
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        self.model = tf.keras.Model(inputs=base_model.input, outputs=x)
        self.scaler = StandardScaler()

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

        features = features / np.linalg.norm(features, axis=1, keepdims=True)

        for i, img_path in enumerate(img_paths):
            features_dict[img_path] = features[i]

        return features_dict

    def save_features(self, features_dict, save_path):
        print(f"Saving features to {save_path}. Please wait...")
        with open(save_path, 'wb') as f:
            pkl.dump(features_dict, f)
