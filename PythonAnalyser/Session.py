import math

import numpy as np

import AppSettings


class Session:
    def __init__(self, file_prefix):
        '''
        Initlise a session from a file prefix

        :param file_prefix: the data prefixes
        '''
        file_prefix_split = file_prefix.split("_")
        self.IMEI = file_prefix_split[0].split("/")[-1] #  set the IMEI number
        self.start_time = file_prefix_split[1]  # set the start time of the session
        self.accel_filename = file_prefix + "_accel.txt"  # get the accelerometer filename
        self.gyro_filename = file_prefix + "_gyro.txt"  # set the gyroscope data file name
        self.rota_filename = file_prefix + "_rota.txt"  # set the rotation vector file name
        self.set_list_from_file()  # get raw data
        self.accels_raw = self.accels_raw[self.accels_raw[:, 0].argsort(kind='mergesort')]  # sort accelerometer by timestamp
        self.gyros_raw = self.gyros_raw[self.gyros_raw[:, 0].argsort(kind='mergesort')]  # sort gyroscope by timestamp
        self.rotas_raw = self.rotas_raw[self.rotas_raw[:, 0].argsort(kind='mergesort')]  # sort rotational vector by time stamps
        self.label = file_prefix_split[0].replace(AppSettings.get_model_data_dir(),"").replace(AppSettings.get_new_data_dir(),"").split("\\")[0]  # get the directory/label
        self.name = file_prefix_split[-1]  # get the name of the user

    @staticmethod
    def get_list_from_file(line):
        '''
        Get the raw data from file line

        :param line: line from file
        :return:
        '''
        line = line.replace("\n","")  # remove new line char at the end of each line
        ls = line.split(",")  # split by comma
        r = np.empty([len(ls)])
        for i in range(len(ls)):  # for each item in the line
            if i == 0:
                r[i] = np.longlong(ls[i])  # set the timestampt to a long
            else:
                r[i] = float(ls[i])  # set everything else to float
        return r

    def set_list_from_file(self):
        '''
        Set all the raw data from the filenames

        :return:
        '''
        accel_file = open(self.accel_filename, 'r')  # open the accel file
        accel_lines = accel_file.readlines()  # read all lines
        self.accels_raw = np.empty([len(accel_lines), 4])  # initilize empty array
        for i in range(len(accel_lines)):  # for each line
            self.accels_raw[i] = self.get_list_from_file(accel_lines[i])  # set an item in the array

        gyro_file = open(self.gyro_filename, 'r')  # open the gyroscope file
        gyro_lines = gyro_file.readlines()  # read all lines
        self.gyros_raw = np.empty([len(gyro_lines), 4])  # init empty array
        for i in range(len(gyro_lines)):  # for each line
            self.gyros_raw[i] = self.get_list_from_file(gyro_lines[i])  # set raw data

        rota_file = open(self.rota_filename, 'r')  # open roational vector file
        rota_lines = rota_file.readlines()  # read all the lines
        self.rotas_raw = np.empty([len(rota_lines), 6])  # init raw array
        for i in range(len(rota_lines)):  # for each line
            l = self.get_list_from_file(rota_lines[i])  # get tje values from the line
            self.rotas_raw[i] = [l[0],math.degrees(l[1]),math.degrees(l[2]),math.degrees(l[3]),l[4],l[5]]  # convert xyz to degrees
