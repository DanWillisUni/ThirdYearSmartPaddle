import Utilities
import AppSettings
from Sensors import SensorIn as si
import DataHandling as dh

import os
import numpy as np


if __name__ == '__main__':
    features = None
    labels = None
    dir_names = ["Perfect","Over-Reaching","Not-Upright","Stroke-To-Shallow","Stroke-To-Wide","Blade-Angle-Wrong","Test"]
    for dir_name in dir_names:
        filename_list = Utilities.get_filenames(os.path.join(AppSettings.get_model_data_dir(), dir_name))
        for filename in filename_list:
            session = si.Session(filename)
            current_features ,current_labels = dh.feature_extraction(session)
            if features is None:
                features = np.array(current_features)
            else:
                features = np.append(features, [current_features])

            if labels is None:
                labels = np.array(current_labels)
            else:
                labels = np.append(labels, current_labels, axis=0)
    features = features.reshape([-1,6])
    labels = labels.reshape([-1,1])
    dh.five_fold_cross_validation(features,labels)