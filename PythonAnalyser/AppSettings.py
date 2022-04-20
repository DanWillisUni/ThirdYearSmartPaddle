
paddle_types = {
	"Perfect":0,
	"Over-Reaching":1,
	"Not-Upright":2,
	#"Stroke-Too-Shallow":3,
	"Stroke-Too-Wide":3,
	"Blade-Angle-Wrong":4
}


def get_new_data_dir():
	return "res/DATA/AppData/"


def get_model_data_dir():
	return "res/DATA/ModelData/"


def get_image_dir():
	return "res/Images/"


def get_dirs():
	return ["Perfect", "Over-Reaching", "Not-Upright", "Stroke-Too-Wide", "Blade-Angle-Wrong"]


def get_window_size():
	return 16
