import sys
import os
import time

sys.path.append("..")
from scservo_sdk import *                   # Uses FTServo SDK library
from scservo_sdk.sms_sts import *

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
new_id = 4  # 设定新的舵机ID


# # id config + 验证位置
# sts.configure_servo_id(1, new_id)
# sts.verify_zero_position(new_id)

# # 多舵机同步控制示例
# SERVO_IDS = [1, 2, 3, 4]      # 舵机ID数组
# ERROR_THRESHOLD = 5           # 位置误差允许值（±5）
# target_positions = [0, 0, 4000, 4000]  # 目标位置数组，与ID一一对应
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
[2501, 2000, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2500, 2502, 2502]
[1:5PP 2:3DP 3:2DP 4:2PP 5:2AP 6:5DP 7:5AP 8:3AP 9:1AAP 10:1AP 11:1DP 12:1PP 13:3PP 14:4PP 15:4DP 16:4AP]
[2501-3200, 1400-2000, 2100-2495, 2502-3100, 2005-2200, 2000-2400, 2489-2700, 2504-3000, 2500-3000, 2499-3000, 2100-2503, 2497-3000, 2000-2500, 1900-2500, 2000-2502, 2000-2502]
[3200, 1400, 2100, 3100, 2200, 2400, 2700, 3000, 2500, 3000, 2100, 3000, 2000, 1900, 2000, 2000]
# '''
# target_positions = [2501, 1900, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2400, 2400, 2400]
# target_positions =[2501, 2000, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2500, 2502, 2502]
# 防止线脱 
target_positions =[2501, 1900, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2400, 2400, 2400]
# 收紧 
target_positions =[3200, 1200, 2100, 3200, 2200, 2400, 2700, 2700, 2500, 3000, 2100, 2500, 1700, 2000, 2000, 2200]
# 拼旁求：
# target_positions =[2501, 1700, 2350, 3100, 2005, 2000, 2489, 2500, 2700, 2800, 23000, 2900, 1900, 2500, 2502, 2500]
# [[水瓶：
# target_positions =[2800, 1200, 1900, 3000, 2005, 2300, 2700, 2700, 2500, 2600, 1900, 2911, 1900, 2000, 2000, 2200]
# 弹簧：
# target_positions =[3000, 1600, 2000, 2900, 2005, 2000, 2700, 2700, 2800, 2800, 2000, 2750, 1800, 1950, 2100, 2100]
# [[图钉：
# target_positions =[2501, 2000, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2500, 2502, 2502]
# 卡套：
# target_positions =[2600, 1400, 2100, 2900, 2005, 2000, 2700, 2500, 2500, 2600, 2200, 3000, 2000, 2100, 2100, 2400]
# 奶牛：
# target_positions =[2900, 1600, 1900, 2900, 1800, 2000, 2700, 2500, 3000, 2800, 2000, 2750, 1800, 1950, 2100, 2500]
# 布料：
# target_positions =[2501, 1500, 2200, 3100, 2005, 2000, 2489, 2700, 2900, 2800, 2200, 2700, 2000, 2500, 2502, 2500]
# 尼龙绳：
# target_positions =[2501, 1500, 2200, 3100, 2005, 2000, 2489, 2700, 2900, 2800, 2200, 2700, 2000, 2500, 2502, 2500]
# 图钉：
# target_positions =[3000, 1400, 2100, 2800, 2200, 2200, 2489, 2500, 2800, 2700, 2000, 3000, 1900, 1900, 2502, 2500]
# mofang:
# target_positions =[2900, 1600, 2100, 3100, 2400, 2100, 2489, 2504, 2700,2500, 2200, 3000, 2000, 2000, 2200, 2400]
# target_positions =[3000, 1400, 2000, 3000, 1800, 2200, 2489, 2500, 2800, 2700, 2000, 3000, 1900, 1900, 2502, 2300]



# target_positions =[2501, 1900, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2400, 2400, 2400]
# target_positions =[2501, 2000, 2495, 2502, 2005, 2000, 2489, 2504, 2500, 2499, 2503, 2497, 2500, 2500, 2502, 2502]
pos_results, initial_pos_array, all_success = sts.read_multi_positions(SERVO_IDS)  # 读取初始位置
sts.multi_servos_to_target(SERVO_IDS, target_positions, speed=1000, acc=200)  # 同步控制到目标位置
sts.verify_movements_to_target(SERVO_IDS, target_positions)  # 验证是否到达目标位置
# Calibrate_Pos = POSE_LIST[0]
# pos_change_array = cal_pos_change(INITIAL_POS_ARRAY , target_positions)  # 计算位置变化量
# pose_dict = name_pos_dict(Calibrate_Pos, pos_change_array)  # 创建命名位姿字典
# save_success = save_pos_json(pose_dict, filename="pose_changes.json", mode="update")  # 保存到JSON文件
# if save_success:
#     print("位姿变化量成功保存到 pose_changes.json")


# loaded_poses = load_pos("pose_changes.json", POSE_LIST[0])  # 从JSON文件加载位姿数据
# print(f"从JSON加载的位姿数据: {loaded_poses}")

# Calibrate_Pos = POSE_LIST[9]   # 比如 "球" 或其它
# pose_dict = name_pos_dict(Calibrate_Pos, target_positions)

# save_success = save_pos_json(
#     pose_dict,
#     filename="pose_targets.json",   # 新文件名，表示存的是目标位置
#     mode="update"
# )
# if save_success:
#     print("位姿目标矩阵成功保存到 pose_targets.json")

# # 3. 测试读回来看
# loaded_pose_array, _ = load_pos("pose_targets.json", Calibrate_Pos)
# print(f"从JSON加载的目标矩阵: {loaded_pose_array}")