import model as m
import Utilities
import Session as si
import DataHandling as dh
import AppSettings

import numpy as np

if __name__ == '__main__':
    clf = m.get_model()  # get the model
    print("=====Test Data=====")
    filename_list = Utilities.get_filenames(AppSettings.get_new_data_dir())  # search for files
    names = list()
    sessions = list()
    for filename in filename_list:  # for each filename
        session = si.Session(filename)  # create a session
        sessions.append(session)  # add session to list
        if not names.__contains__(session.name):  # if the name isnt in names list
            names.append(session.name)  # add name to names list

    for name in names:  # for each name in the name list
        features = None
        for session in sessions:  # for each session
            if session.name == name:  # if the session name is the one being processed
                current_features, current_labels = dh.feature_extraction(session)  # extract features from session
                if current_features is not None:
                    if features is None:
                        features = np.array(current_features)  # create array with features in
                    else:
                        features = np.append(features, current_features, axis=0)  # add current features to features
        for i in range(0, np.size(features, axis=1)):  # for each feature
            dh.plot_extracted_features(features,name + "/",i)  # plot feature
        label_count = m.classify(clf, features)  # classify all features
        print(name + " " + str(m.classify_readable(label_count)))  # print readable output
