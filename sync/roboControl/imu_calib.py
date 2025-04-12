from mpu6050 import mpu6050
import numpy as np

imu = mpu6050(0x68)
gyro_labels = ['w_x', 'w_y', 'w_z']  # gyro labels for plots
cal_size = 500  # points to use for calibration

def  imu_offsets():
    print("-"*50)
    print('IMU Calibrating - Stay Steady!')
    accel_data_array = []
    gyro_data_array = []
    accel_offsets = [0.0,0.0,0.0]
    gyro_offsets = [0.0,0.0,0.0]
    while True:

        accel_data = imu.get_accel_data()
        gyro_data = imu.get_gyro_data()

        accel_data_array.append([accel_data['x'], accel_data['y'], accel_data['z']])
        gyro_data_array.append([gyro_data['x'], gyro_data['y'], gyro_data['z']])

        if np.shape(accel_data_array)[0] == cal_size:
            for i in range(0,3):
                accel_offsets[i] = np.mean(np.array(accel_data_array)[:,i])
            for i in range(0,3):
                gyro_offsets[i] = np.mean(np.array(gyro_data_array)[:,i])
            break
    print('Gyro Calibration Complete')
    return accel_offsets, gyro_offsets
