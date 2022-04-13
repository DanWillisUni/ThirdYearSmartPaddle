import Utilities
import AppSettings as set
from Sensors import SensorIn as si
import DataHandling as dh
import os
import numpy as np


if __name__ == '__main__':
    l = Utilities.get_filenames(os.path.join(set.get_model_data_dir(), "Perfect"))
    s = si.Session(l[0])
    f = dh.feature_extraction(s)
    for i in range(np.size(f,1)):
        dh.plot_extracted_features(f,"Perfect",i)

    l = Utilities.get_filenames(set.get_new_data_dir())
    s = si.Session(l[0])
    f = dh.feature_extraction(s)
    for i in range(np.size(f,1)):
        dh.plot_extracted_features(f, "Andrew", i)