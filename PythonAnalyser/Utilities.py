import os


def get_filenames(dir):
	r = list()
	for p in os.listdir(dir):
		p_split = p.split("_")
		file_prefix = '_'.join(p_split[:-1])
		if os.path.join(dir, file_prefix) not in r:
			r.append(os.path.join(dir, file_prefix))
	return r
