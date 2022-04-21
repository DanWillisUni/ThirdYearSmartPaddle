import Utilities
import AppSettings
import Session as si
import DataHandling as dh

import os
import numpy as np


def get_model():
    '''
    Gets and trains the model

    :return: model
    '''
    features = None
    labels = None
    dir_names = AppSettings.get_dirs()  # get the list of directory names
    for dir_name in dir_names:  # for each directory
        filename_list = Utilities.get_filenames(os.path.join(AppSettings.get_model_data_dir(), dir_name))  # get the list of files
        dir_features = None
        for filename in filename_list:  # for each file
            session = si.Session(filename)  # create new session
            current_features, current_labels = dh.feature_extraction(session)  # extract features
            # add features to the dirs running amount
            if dir_features is None:
                dir_features = np.array(current_features)
            else:
                dir_features = np.append(dir_features, current_features,axis=0)
            # add the correct label to the array
            if labels is None:
                labels = np.array(current_labels)
            else:
                labels = np.append(labels, current_labels, axis=0)
        for i in range(0, np.size(dir_features, axis=1)):  # for each feature
            dh.plot_extracted_features(dir_features, dir_name + "/", i)  # plot the feature of the dir data
        # add the dir features to the whole features array
        if features is None:
            features = np.array(dir_features)
        else:
            features = np.append(features, dir_features,axis=0)

    labels = labels.reshape([-1])  # reshape labels
    confusion_matrix, clf = dh.five_fold_cross_validation(features, labels)  # get and build model

    for i in range(0,len(dir_names)):  # for each directory
        print("Precision " + dir_names[i] + ": " + str(calculate_precision(confusion_matrix, i)))  # calculate precision
        print("Recall " + dir_names[i] + ": " + str(calculate_recall(confusion_matrix, i)))  # calcualte recall
    print("Accuracy: " + str(calculate_accuracy(confusion_matrix)))  # calculate accuracy

    return clf  # return model


def classify(clf,features):
    '''
    Classify a bunch of features

    :param clf: model
    :param features: features
    :return: label count
    '''
    label_count = [0] * len(AppSettings.get_dirs())
    predicted_label = clf.predict(features)  # predict all features
    predicted_labels = predicted_label.flatten().tolist()  # flatten labels to list
    for predicted_label in predicted_labels:  # for each prediction
        label_count[AppSettings.paddle_types[predicted_label]] += 1  # add 1 to the paddle type that the label is
    return label_count  # return the count


def calculate_precision(confusion_matrix, index):
    '''
    Calculate the precision from the confusion matrix

    TP / (TP+FP)
    :param confusion_matrix: confusion matrix
    :param index: index of paddle type to calculate
    :return: precision
    '''
    tp = 0
    fp = 0
    for predicted_value_index in range(0, len(confusion_matrix[0])):  # for each predicted value
        if predicted_value_index == index:  # if the predicted value index os the index we are searching for
            tp += confusion_matrix[index][predicted_value_index]  # add to true posotive
        else:
            fp += confusion_matrix[index][predicted_value_index]  # add to false posotive
    #print("True Positive: " + str(tp))
    #print("False Positive: " + str(fp))
    return tp / (tp + fp)  # calculate


def calculate_recall(confusion_matrix, index):
    '''
    Calculate recall of paddle type from confusion matrix

    TP / (TP+FN)
    :param confusion_matrix: confusion matrix
    :param index: index of paddle type
    :return: recall
    '''
    tp = 0
    fn = 0
    for true_value_index in range(0, len(confusion_matrix)): # for each true value index
        if true_value_index == index:  # if the true value is the index searching for
            tp += confusion_matrix[true_value_index][index]  # add the number of true posotives
        else:
            fn += confusion_matrix[true_value_index][index]  # add to the number of false negatives
    #print("True Positive: " + str(tp))
    #print("False Negative: " + str(fn))
    return tp / (tp + fn) # calculate


def calculate_accuracy(confusion_matrix):
    '''
    Calculate the accuracy of the model using confusion matrix

    :param confusion_matrix: confusion matrix
    :return: accuracy
    '''
    t = 0
    f = 0
    for true_value_index in range(0, len(confusion_matrix)):  # for each true value index
        for predicted_value_index in range(0, len(confusion_matrix)):  # for each predicted vaue index
            if true_value_index == predicted_value_index:  # if the true value = predicted value
                t += confusion_matrix[true_value_index][predicted_value_index]  # add the value to true total
            else:
                f += confusion_matrix[true_value_index][predicted_value_index]  # add the value to false total
    #print("True: " + str(t))
    #print("False: " + str(f))
    return t / (t + f)


def classify_readable(label_count):
    '''
    Convert to label count into something readable

    :param label_count: the frequency of labels assigned during classification
    :return: Sentance of feedback
    '''
    total = label_count[0]  # set the total to the number of perfects
    index_of_highest = 1
    for i in range(1,len(label_count)):  # for every label frequency except perfect
        total += label_count[i]  # add the label frequency to total
        if label_count[i]>label_count[index_of_highest]:  # if the frequency is higher than the previous highest
            index_of_highest = i  # update the highest index
    return "Perfect " + str(round(100*((float)(label_count[0]/total)),2)) + "%, to improve " + AppSettings.get_dirs()[index_of_highest] + " " + str(round(100* label_count[index_of_highest]/total,2)) +"% " + str(label_count)  # coherent sentance