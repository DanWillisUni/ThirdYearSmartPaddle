import model as m
import Utilities
import Session as si
import DataHandling as dh
import AppSettings

import numpy as np

if __name__ == '__main__':
    clf = m.get_model()
    print("=====Test Data=====")
    filename_list = Utilities.get_filenames(AppSettings.get_new_data_dir())
    names = list()
    sessions = list()
    for filename in filename_list:
        session = si.Session(filename)
        sessions.append(session)
        if not names.__contains__(session.name):
            names.append(session.name)

    for name in names:
        features = None
        for session in sessions:
            if session.name == name:
                current_features, current_labels = dh.feature_extraction(session)
                if features is None:
                    features = np.array(current_features)
                else:
                    features = np.append(features, current_features, axis=0)
        for i in range(0,np.size(features,axis=1)):
            dh.plot_extracted_features(features,name + "/Feature",i)
        label_count = m.classify(clf, features)
        print(name + " " + str(m.classify_readable(label_count)))
