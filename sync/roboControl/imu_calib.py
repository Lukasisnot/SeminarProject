from mpu6050 import mpu6050

imu = mpu6050(0x68)
calib_points = 200

def  imu_offsets():
    print('IMU Calibration Started')
    accel_offsets = [0.0,0.0,0.0]
    gyro_offsets = [0.0,0.0,0.0]
    accel_data_array = []
    gyro_data_array = []

    for _ in range(calib_points):
        accel_data = imu.get_accel_data()
        gyro_data = imu.get_gyro_data()

        accel_data_array.append([accel_data['x'], accel_data['y'], accel_data['z']])
        gyro_data_array.append([gyro_data['x'], gyro_data['y'], gyro_data['z']])

    print('Calibration points gathered, calculating offsets')

    for i in range(calib_points):
        for k in range(0,3):
            accel_offsets[k] += accel_data_array[i][k]
        for k in range(0,3):
            gyro_offsets[k] += gyro_data_array[i][k]

    for i in range(3):
        accel_offsets[i] /= calib_points
        gyro_offsets[i] /= calib_points

    accel_offsets[0] += 9.81

    print('IMU Calibration Complete')
    return accel_offsets, gyro_offsets
