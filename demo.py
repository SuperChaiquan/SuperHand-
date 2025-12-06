import sys
import os
import time

sys.path.append("..")
from scservo_sdk import *                   # Uses FTServo SDK library


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler('/dev/ttyACM0') #ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

# Initialize PacketHandler instance
# Get methods and members of Protocol
sts = sms_sts(portHandler)
# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate 1000000
if portHandler.setBaudRate(1000000):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()


# id config + 验证位置
# new_id = 7  # 设定新的舵机ID
# sts.configure_servo_id(1, new_id)
# sts.verify_zero_position(new_id)

# 多舵机同步控制示例 [2048, 4000, 4000,2048, 2048, 2048, 2048] 
# SERVO_IDS = [1, 2, 3, 4,5,6,7]      # 舵机ID数组
# ERROR_THRESHOLD = 5           # 位置误差允许值（±5）
# target_positions = [0, 0, 0, 0, 0, 0, 0] # 目标位置数组，与ID一一对应
# sts.multi_servos_to_target(SERVO_IDS, target_positions, speed=1000, acc=200)  # 同步控制到目标位置
# sts.verify_movements_to_target(SERVO_IDS, target_positions, error_threshold=ERROR_THRESHOLD)  # 验证是否到达目标位置


# Workflow example
'''
caliberate initial positions
adjust to target positions
calculate relative position transfer
save to json 
load from json
execute movements
'''
SERVO_IDS = [1, 2, 3, 4,5,6,7]      # 舵机ID数组
ERROR_THRESHOLD = 5           # 位置误差允许值（±5）
target_positions = [2048, 4000, 4000,2048, 2048, 2048, 2048]  # 目标位置数组，与ID一一对应

pos_results, initial_pos_array, all_success = sts.read_multi_positions(SERVO_IDS)  # 读取初始位置
sts.multi_servos_to_target(SERVO_IDS, target_positions, speed=3000, acc=255)  # 同步控制到目标位置
sts.verify_movements_to_target(SERVO_IDS, target_positions, error_threshold=ERROR_THRESHOLD)  # 验证是否到达目标位置

pos_change_array = cal_pos_change(initial_pos_array, target_positions)  # 计算位置变化量
pose_dict = name_pos_dict("拿卡", pos_change_array)  # 创建命名位姿字典
save_success = save_pos_json(pose_dict, filename="pose_changes.json", mode="update")  # 保存到JSON文件
if save_success:
    print("位姿变化量成功保存到 pose_changes.json")
loaded_poses = load_pos("pose_changes.json","抓球")  # 从JSON文件加载位姿数据
print(f"从JSON加载的位姿数据: {loaded_poses}")