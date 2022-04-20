import math
import os.path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import itertools
from sklearn.feature_selection import RFE
from scipy.signal import find_peaks

import AppSettings

#def smooth_raw(session):


def feature_extraction(session):
	'''
	Extracts features from raw data

	:param session: session to look at
	:return: features extracted with label
	'''
	features = None
	labels = None

	segment_size = AppSettings.get_window_size()  # The window size for feature extraction
	full_length = segment_size * math.floor(len(session.accels_raw)/segment_size)
	for i in range(0, full_length - segment_size, int(segment_size / 2)):  # for each segment
		accel_seg = session.accels_raw[i:i + segment_size, :]  # gets the segment of data for accelerometer
		accel_vals = np.delete(accel_seg, 0, 1)  # cuts of the timestamps
		accel_mag = np.sqrt((accel_vals[:, 0] ** 2).reshape(-1, 1) + (accel_vals[:, 1] ** 2).reshape(-1, 1) + (accel_vals[:, 2] ** 2).reshape(-1, 1))  # get the magnitude of xyz combined into one
		accel_mag_mean = np.mean(accel_mag)  # mean magnitude
		accel_mag_var = np.var(accel_mag)  # varience in magnitude

		gyro_seg = session.gyros_raw[i:i + segment_size, :]  # get the gyro segment
		gyro_vals = np.delete(gyro_seg, 0, 1)  # cut the time column out
		gyro_mag = np.sqrt((gyro_vals[:, 0] ** 2).reshape(-1, 1) + (gyro_vals[:, 1] ** 2).reshape(-1, 1) + (gyro_vals[:, 2] ** 2).reshape(-1, 1))  # get the magnitude of the xyz of the gyroscope
		gyro_mean = np.mean(gyro_mag)  # get the mean
		gyro_var = np.var(gyro_mag)  # get the varience

		rota_seg = session.rotas_raw[i:i + segment_size, :]  # get the rotation vector segment
		rota_vals = np.delete(rota_seg, 0, 1)  # delete the timestamps
		rota_vals = np.delete(rota_vals, 3, 1)  # delete the third value
		rota_vals = np.delete(rota_vals, 3, 1)  # delete the heading

		rota_xy_vals = np.delete(rota_vals,2,1)  # delete z value
		rota_xy_mag = np.sqrt((rota_xy_vals[:, 0] ** 2).reshape(-1, 1) + (rota_xy_vals[:, 1] ** 2).reshape(-1, 1))  # get xy combined
		rota_xy_mean = np.mean(rota_xy_mag)  # get xy mean
		rota_xy_var = np.var(rota_xy_mag)  # get xy varience

		rota_z_vals = np.delete(rota_vals, 0, 1)  # delete x
		rota_z_vals = np.delete(rota_z_vals, 0, 1)  # delete y
		rota_z_mean = np.mean(rota_z_vals)  # get z mean
		rota_z_var = np.var(rota_z_vals)  # get z varience

		rota_z_sum_dif = 0
		gyro_mag_sum_dif = 0
		for j in range(0, segment_size - 1):  # for every segment
			rota_z_sum_dif += abs(rota_z_vals[j] - rota_z_vals[j + 1])  # get the difference between the z
			gyro_mag_sum_dif += abs(gyro_mag[j] - gyro_mag[j+1])

		feature = [accel_mag_mean, accel_mag_var, gyro_mean, gyro_var, rota_xy_mean, rota_xy_var,rota_z_mean,rota_z_var,rota_z_sum_dif[0],gyro_mag_sum_dif[0]]  # set all features in one array
		##add feature to features
		if features is None:
			features = np.array([feature])
		else:
			features = np.append(features, [feature], axis=0)
		##add label to labels
		if labels is None:
			labels = np.array([session.label])
		else:
			labels = np.append(labels, [session.label], axis=0)

	return features, labels


def plot_extracted_features(features, prefix, i):
	'''
	Plot features onto graph and save them as pngs

	:param features: all features
	:param prefix: file prefix
	:param i: index of feature to plot
	'''
	plt.plot(features[:, i])  # plots features of index i
	plt.xticks(fontsize=8)
	plt.yticks(fontsize=8)
	if i == 0 or i == 1:  # setting titles and graph units etc
		plt.ylabel('m/s^2', fontsize=8)
		if i == 0:
			plt.gca().set_title('Mean acceleration', fontsize=8)
		else:
			plt.gca().set_title('Var acceleration', fontsize=8)
	if i == 2 or i == 3:
		plt.ylabel('rad/s', fontsize=8)
		if i == 2:
			plt.gca().set_title('Mean Gyroscope', fontsize=8)
		else:
			plt.gca().set_title('Var Gyroscope', fontsize=8)
	if i == 4 or i == 5 or i == 6 or i==7:
		#plt.ylabel('rad/s', fontsize=8)
		if i == 4:
			plt.gca().set_title('Mean Rotation Vector XY', fontsize=8)
		elif i == 5:
			plt.gca().set_title('Var Rotation Vector XY', fontsize=8)
		elif i == 6:
			plt.gca().set_title('Mean Rotation Vector Z', fontsize=8)
		else:
			plt.gca().set_title('Var Rotation Vector Z', fontsize=8)

	plt.grid(True)
	if not os.path.exists(AppSettings.get_image_dir() + prefix):  # if directories dont exist
		os.makedirs(AppSettings.get_image_dir() + prefix)  # create directories
	plt.savefig(AppSettings.get_image_dir() + prefix + " " + str(i + 1) + " Feature Data.png")  # save
	#print("Save Feature " + str(i + 1) + " Data")
	plt.close()


def five_fold_cross_validation(features, labels):
	'''
	Create and train model

	Calculate confusion matrix
	:param features: features extracted
	:param labels: labels extracted
	:return: the confusion matrix and model
	'''
	true_labels = list()
	predicted_labels = list()
	for train_index, test_index in StratifiedKFold(n_splits=5).split(features, labels):  # split features and labels for train and test
		X_train = features[train_index, :]
		Y_train = labels[train_index]
		X_test = features[test_index, :]
		Y_test = labels[test_index]

		clf = DecisionTreeClassifier()  # construct classifier
		clf.fit(X_train, Y_train)  # train clasifier
		predicted_label = clf.predict(X_test)  # predict

		predicted_labels += predicted_label.flatten().tolist()  # set prediction labels
		true_labels += Y_test.flatten().tolist()  # set true labels
	confusion_matrix = np.zeros((len(AppSettings.paddle_types), len(AppSettings.paddle_types)))  # construct confusion matrix

	for i in range(len(true_labels)):  # for each peice of data
		confusion_matrix[AppSettings.paddle_types[true_labels[i]], AppSettings.paddle_types[predicted_labels[i]]] += 1  # populate confusion matrix

	plot_confusion_matrix(confusion_matrix, AppSettings.paddle_types.keys(), normalize=True)  # plot confusion matrix
	plt.savefig(AppSettings.get_image_dir() + "Confusion_Matrix.png")  # save confusion matrix plot
	print("Save Confusion Matrix")
	plt.close()

	selector = RFE(clf, n_features_to_select=1)  # select 1 feature to rank properly
	selector.fit(X_train, Y_train)  # fit
	print(selector.ranking_)  # print ranking

	return confusion_matrix, clf


def plot_confusion_matrix(confusion_matrix, classes, normalize=False, title='Confusion Matrix', cmap=plt.cm.Blues):
	'''
	This function prints and plots the confusion matrix

	:param confusion_matrix: filled in confusion matrix
	:param classes: Name of all the classes possible to be classified into
	:param normalize: Is the matrix normalised
	:param title: title of the figure
	:param cmap: Colour map to use
	'''
	if normalize:  # if its normalised
		confusion_matrix = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]  # convert to probabilities
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	print(confusion_matrix)

	plt.imshow(confusion_matrix, interpolation='nearest', cmap=cmap)  # plot with colour map
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalize else '.0f'
	thresh = confusion_matrix.max() / 2.
	for i, j in itertools.product(range(confusion_matrix.shape[0]), range(confusion_matrix.shape[1])):  # iterate confusion matrix
		plt.text(j, i, format(confusion_matrix[i, j], fmt), horizontalalignment="center", color="white" if confusion_matrix[i, j] > thresh else "black")  # put text over
	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
