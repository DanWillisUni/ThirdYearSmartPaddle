import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import StratifiedKFold
from sklearn.tree import DecisionTreeClassifier
import itertools
from sklearn.feature_selection import RFE

import AppSettings


def feature_extraction(session):
	features = None
	labels = None

	segment_size = 16  # The window size for feature extraction
	for i in range(0, len(session.accels) - segment_size, int(segment_size / 2)):
		accel_seg = session.accels[i:i + segment_size, :]
		accel_vals = np.delete(accel_seg, 0, 1)
		accel_mean = np.mean(accel_vals)
		accel_var = np.var(accel_vals)

		gyro_seg = session.gyros[i:i + segment_size, :]
		gyro_vals = np.delete(gyro_seg, 0, 1)
		gyro_mean = np.mean(gyro_vals)
		gyro_var = np.var(gyro_vals)

		rota_seg = session.rotas[i:i + segment_size, :]
		rota_vals = np.delete(rota_seg, 0, 1)
		rota_vals = np.delete(rota_vals, 3, 1)
		rota_vals = np.delete(rota_vals, 3, 1)

		rota_xy_vals = np.delete(rota_vals,2,1)
		rota_xy_mean = np.mean(rota_xy_vals)
		rota_xy_var = np.var(rota_xy_vals)

		rota_z_vals = np.delete(rota_vals, 0, 1)
		rota_z_vals = np.delete(rota_z_vals, 0, 1)
		rota_z_mean = np.mean(rota_z_vals)
		rota_z_var = np.var(rota_z_vals)

		feature = [accel_mean, accel_var, gyro_mean, gyro_var, rota_xy_mean, rota_xy_var,rota_z_mean,rota_z_var]
		if features is None:
			features = np.array([feature])
		else:
			features = np.append(features, [feature], axis=0)

		if labels is None:
			labels = np.array([session.label])
		else:
			labels = np.append(labels, [session.label], axis=0)

	return features, labels


def plot_extracted_features(features, prefix, i):
	plt.plot(features[:, i])
	plt.xticks(fontsize=8)
	plt.yticks(fontsize=8)
	if i == 0 or i == 1:
		plt.ylabel('m/s^2', fontsize=8)
		if i == 0:
			plt.gca().set_title('Mean acceleration', fontsize=8)
		else:
			plt.gca().set_title('Var acceleration', fontsize=8)
	if i == 2 or i == 3:
		plt.ylabel('rad/s', fontsize=8)
		if i == 0:
			plt.gca().set_title('Mean Gyroscope', fontsize=8)
		else:
			plt.gca().set_title('Var Gyroscope', fontsize=8)

	plt.grid(True)
	plt.savefig(AppSettings.get_image_dir() + prefix + " " + str(i + 1) + " Feature Data.png")
	print("Save Feature " + str(i + 1) + " Data")
	plt.close()


def five_fold_cross_validation(features, labels):
	true_labels = list()
	predicted_labels = list()
	for train_index, test_index in StratifiedKFold(n_splits=5).split(features, labels):
		X_train = features[train_index, :]
		Y_train = labels[train_index]
		X_test = features[test_index, :]
		Y_test = labels[test_index]

		clf = DecisionTreeClassifier()
		clf.fit(X_train, Y_train)
		predicted_label = clf.predict(X_test)

		predicted_labels += predicted_label.flatten().tolist()
		true_labels += Y_test.flatten().tolist()
	confusion_matrix = np.zeros((len(AppSettings.paddle_types), len(AppSettings.paddle_types)))

	for i in range(len(true_labels)):
		confusion_matrix[AppSettings.paddle_types[true_labels[i]], AppSettings.paddle_types[predicted_labels[i]]] += 1

	plot_confusion_matrix(confusion_matrix, AppSettings.paddle_types.keys(), normalize=False)
	plt.savefig(AppSettings.get_image_dir() + "Confusion_Matrix.png")
	print("Save Confusion Matrix")
	plt.close()

	selector = RFE(clf, n_features_to_select=1)
	selector.fit(X_train, Y_train)
	print(selector.ranking_)

	return confusion_matrix, clf


def plot_confusion_matrix(confusion_matrix, classes, normalize=False, title='Confusion Matrix', cmap=plt.cm.Blues):
	""" This function prints and plots the confusion matrix.
        Normalization can be applied by setting `normalize=True`.
    """
	if normalize:
		confusion_matrix = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]
		print("Normalized confusion matrix")
	else:
		print('Confusion matrix, without normalization')

	print(confusion_matrix)

	plt.imshow(confusion_matrix, interpolation='nearest', cmap=cmap)
	plt.title(title)
	plt.colorbar()
	tick_marks = np.arange(len(classes))
	plt.xticks(tick_marks, classes, rotation=45)
	plt.yticks(tick_marks, classes)

	fmt = '.2f' if normalize else '.0f'
	thresh = confusion_matrix.max() / 2.
	for i, j in itertools.product(range(confusion_matrix.shape[0]), range(confusion_matrix.shape[1])):
		plt.text(j, i, format(confusion_matrix[i, j], fmt), horizontalalignment="center", color="white" if confusion_matrix[i, j] > thresh else "black")
	plt.tight_layout()
	plt.ylabel('True label')
	plt.xlabel('Predicted label')
