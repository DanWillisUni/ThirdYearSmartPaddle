import model as m
import Utilities
from Sensors import SensorIn as si
import DataHandling as dh
import AppSettings

import os
import numpy as np

if __name__ == '__main__':
    clf = m.get_model()
    print("=====Test Data=====")
    filename_list = Utilities.get_filenames(AppSettings.get_new_data_dir())
    for filename in filename_list:
        session = si.Session(filename)
        current_features, current_labels = dh.feature_extraction(session)
        print(filename + " " + str(m.classify(clf,current_features)))
