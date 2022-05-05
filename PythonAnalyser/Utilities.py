import os


def get_filenames(dir):
	'''
	Gets all the unique filename inside directory

	:param dir: directory to search
	:return: list of filenames
	'''
	r = list()
	if os.path.isdir(dir):  # if the directory exists
		for p in os.listdir(dir):  # for each file path
			p_split = p.split("_")  # split on _
			file_prefix = '_'.join(p_split[:-1])  # join all accept the last one (this removes the accel.txt, gyro.txt and rota.txt from files)
			if os.path.join(dir, file_prefix) not in r:  # if it isnt already in the list
				r.append(os.path.join(dir, file_prefix))  # add to the list
	return r
