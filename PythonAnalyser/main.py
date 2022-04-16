import model as m
import Utilities
import Session as si
import DataHandling as dh
import AppSettings

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
        label_count = [0]*len(AppSettings.get_dirs())
        for session in sessions:
            if session.name == name:
                current_features, current_labels = dh.feature_extraction(session)
                current_label_count = m.classify(clf, current_features)
                label_count = [x + y for x, y in zip(label_count, current_label_count)]
        print(name + " " + str(m.classify_readable(label_count)))
