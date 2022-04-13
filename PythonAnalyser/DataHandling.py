import numpy as np
import matplotlib.pyplot as plt


def feature_extraction(session):

	features = None

	segment_size = 6  # The window size for feature extraction
	for i in range(0, len(session.accels) - segment_size, int(segment_size/2)):
		accel_seg = session.accels[i:i + segment_size, :]
		accel_vals = np.delete(accel_seg,0,1)
		accel_mean = np.mean(accel_vals)
		accel_var = np.var(accel_vals)

		gyro_seg = session.gyros[i:i + segment_size, :]
		gyro_vals = np.delete(gyro_seg,0,1)
		gyro_mean = np.mean(gyro_vals)
		gyro_var = np.var(gyro_vals)

		rota_seg = session.rotas[i:i + segment_size, :]
		rota_vals = np.delete(rota_seg, 0, 1)
		rota_vals = np.delete(rota_vals, 3, 1)
		rota_vals = np.delete(rota_vals, 3, 1)
		rota_mean = np.mean(rota_vals)
		rota_var = np.var(rota_vals)

		feature = [accel_mean, accel_var,gyro_mean,gyro_var,rota_mean,rota_var]
		if features is None:
			features = np.array([feature])
		else:
			features = np.append(features, [feature], axis=0)
	return features


def plot_extracted_features(features,prefix,i):
	plt.plot(features[:, i])
	plt.xticks(fontsize=8)
	plt.yticks(fontsize=8)
	if i == 0 or i==1:
		plt.ylabel('m/s^2', fontsize=8)
		if i == 0:
			plt.gca().set_title('Mean acceleration', fontsize=8)
		else:
			plt.gca().set_title('Var acceleration', fontsize=8)
	if i == 2 or i==3:
		plt.ylabel('rad/s', fontsize=8)
		if i == 0:
			plt.gca().set_title('Mean Gyroscope', fontsize=8)
		else:
			plt.gca().set_title('Var Gyroscope', fontsize=8)

	plt.grid(True)
	plt.savefig("res/Images/" + prefix + " " + str(i + 1) + " Feature Data.png")
	print("Save Feature " + str(i + 1) + " Data")
	plt.close()
