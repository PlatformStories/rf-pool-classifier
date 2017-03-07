# Train a polygon classifier using multispectral imagery and a random forest classifier.
# We are training the classifier to label polygons as 'Contains swimming pool' and 'Does not contain swimming pool'.
# Classification is performed by computing a feature vector per polygon and
# passing feature vector to a Random Forest Classifier.
# Polygons can be of arbitrary shape.

# Task Inputs:
# - train.geojson
# - image.tif
# - n_estimators (string, optional)

import numpy as np
import os
import pickle
import warnings
warnings.filterwarnings('ignore')   # suppress annoying warnings

from shutil import move
from mltools import features
from mltools import geojson_tools as gt
from mltools import data_extractors as de
from gbdx_task_interface import GbdxTaskInterface
from sklearn.ensemble import RandomForestClassifier

class RfPoolClassifier(GbdxTaskInterface):

    def invoke(self):

        # Get inputs
        n_estimators = int(self.get_input_string_port('n_estimators', default = '100'))
        img_dir = self.get_input_data_port('image')
        img = os.path.join(img_dir, os.listdir(img_dir)[0])

        geojson_dir = self.get_input_data_port('geojson')
        geojson = os.path.join(geojson_dir, os.listdir(geojson_dir)[0])


        # Move geojson to same dir as img
        move(geojson, img_dir)

        # Navigate to directory with input data
        os.chdir(img_dir)

        # Create output directory
        output_dir = self.get_output_data_port('trained_classifier')
        os.makedirs(output_dir)

        # Get training data from the geojson input
        train_rasters, train_labels = de.get_data('train.geojson', return_labels=True,
                                                  mask=True)

        # Compute features from each training polygon
        compute_features = features.pool_basic
        X = []
        for raster in train_rasters:
            X.append(compute_features(raster))

        # Create classifier object.
        c = RandomForestClassifier(n_estimators = n_estimators)

        # Train the classifier
        X, train_labels = np.nan_to_num(np.array(X)), np.array(train_labels)
        c.fit(X, train_labels)

        # Pickle classifier and save to output dir
        with open(os.path.join(output_dir, 'classifier.pkl'), 'wb') as f:
            pickle.dump(c, f)


if __name__ == "__main__":
    with RfPoolClassifier() as task:
        task.invoke()
