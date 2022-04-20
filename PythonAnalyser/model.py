import Utilities
import AppSettings
import Session as si
import DataHandling as dh

import os
import numpy as np


def get_model():
	features = None
	labels = None
	dir_names = AppSettings.get_dirs()
	for dir_name in dir_names:
		filename_list = Utilities.get_filenames(os.path.join(AppSettings.get_model_data_dir(), dir_name))
		dir_features = None
		for filename in filename_list:
			session = si.Session(filename)
			current_features, current_labels = dh.feature_extraction(session)
			if dir_features is None:
				dir_features = np.array(current_features)
			else:
				dir_features = np.append(dir_features, current_features,axis=0)

			if labels is None:
				labels = np.array(current_labels)
			else:
				labels = np.append(labels, current_labels, axis=0)
		for i in range(0, np.size(dir_features, axis=1)):  # for each feature
			dh.plot_extracted_features(dir_features, dir_name + "/", i)  # plot feature
		if features is None:
			features = np.array(dir_features)
		else:
			features = np.append(features, dir_features,axis=0)

	labels = labels.reshape([-1])
	confusion_matrix, clf = dh.five_fold_cross_validation(features, labels)

	for i in range(0,len(dir_names)):
		print("Precision " + dir_names[i] + ": " + str(calculate_precision(confusion_matrix, i)))
		print("Recall " + dir_names[i] + ": " + str(calculate_recall(confusion_matrix, i)))
	print("Accuracy: " + str(calculate_accuracy(confusion_matrix)))

	return clf


def classify(clf,features):
	label_count = [0] * 5
	predicted_label = clf.predict(features)
	predicted_labels = predicted_label.flatten().tolist()
	for predicted_label in predicted_labels:
		label_count[AppSettings.paddle_types[predicted_label]] += 1
	return label_count


def calculate_precision(confusion_matrix, index=-1):
    # TP / (TP+FP)
    if index > -1:
        tp = 0
        fp = 0
        for guessed_value in range(0, len(confusion_matrix[0])):
            if guessed_value == index:
                tp += confusion_matrix[index][guessed_value]
            else:
                fp += confusion_matrix[index][guessed_value]
        #print("True Positive: " + str(tp))
        #print("False Positive: " + str(fp))
        return tp / (tp + fp)
    else:
        totalSum = 0.0
        for i in range(0, len(confusion_matrix)):
            totalSum += calculate_precision(confusion_matrix, i)
        return totalSum / len(confusion_matrix)


def calculate_recall(confusion_matrix, index=-1):
    # TP / (TP+FN)
    if index > -1:
        tp = 0
        fn = 0
        for true_value in range(0, len(confusion_matrix)):
            if true_value == index:
                tp += confusion_matrix[true_value][index]
            else:
                fn += confusion_matrix[true_value][index]
        #print("True Positive: " + str(tp))
        #print("False Negative: " + str(fn))
        return tp / (tp + fn)
    else:
        totalSum = 0.0
        for i in range(0, len(confusion_matrix)):
            totalSum += calculate_recall(confusion_matrix, i)
        return totalSum / len(confusion_matrix)


def calculate_accuracy(confusion_matrix):
    t = 0
    f = 0
    for x in range(0, len(confusion_matrix)):
        for y in range(0, len(confusion_matrix)):
            if x == y:
                t += confusion_matrix[x][y]
            else:
                f += confusion_matrix[x][y]
    #print("True: " + str(t))
    #print("False: " + str(f))
    return t / (t + f)

def classify_readable(label_count):
	total = label_count[0]
	indexOfHighest = 1
	for i in range(1,len(label_count)):
		total += label_count[i]
		if label_count[i]>label_count[indexOfHighest]:
			indexOfHighest = i
	return "Perfect " + str(round(100*((float)(label_count[0]/total)),2)) + "%, to improve " + AppSettings.get_dirs()[indexOfHighest] + " " + str(round(100* label_count[indexOfHighest]/total,2)) +"% " + str(label_count)