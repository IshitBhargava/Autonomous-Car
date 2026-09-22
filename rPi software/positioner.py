import math
import carParser

dist = []
theta = 0

back_index = 2
front_index = 1
right_index = 3
left_index = 0

left_offset = 0
right_offset = 0
front_offset = 0
back_offset = 0

theta_calib=0

width = 1183
length = 1141


def convert(dist):
    return [d * math.cos(math.radians(theta)) for d in dist]


def apply_offsets(array):
    result = list(array)
    result[left_index] += left_offset
    result[right_index] += right_offset
    result[front_index] += front_offset
    result[back_index] += back_offset
    return result


carParser.init('/dev/ttyAMA0', 921600)
for i in range(1000):
   imu= carParser.getIMU()
   theta+=imu[8]
   theta_calib/=theta/1000


def test_dists():
    a=float(input("Enter left distance: "))
    b=float(input("Enter right distance: "))
    c=float(input("Enter front distance: "))   
    d=float(input("Enter back distance: "))
    return [a,c,d,b]

def getvals():
    a=float(input("theta: "))
    return [0,0,0,0,0,0,0,0,a]

while True:
    dist = carParser.getDIST()
    #dist= test_dists()       # comment and choose line 51
    dists = apply_offsets(convert(dist))
    imu= carParser.getIMU() # uncomment
    #imu=getvals()    # comment this for live sensor data
    theta=imu[8]-theta_calib
    w_left = 1 / dists[left_index]
    w_right = 1 / dists[right_index]
    w_front = 1 / dists[front_index]
    w_back = 1 / dists[back_index]

    x_from_left = dists[left_index]
    x_from_right = width - dists[right_index]
    y_from_front = length - dists[front_index]
    y_from_back = dists[back_index]

    x_val = (w_left * x_from_left + w_right * x_from_right) / (w_left + w_right)
    y_val = (w_front * y_from_front + w_back * y_from_back) / (w_front + w_back)

    print(x_val, y_val)