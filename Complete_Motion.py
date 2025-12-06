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

pos_results, initial_pos_array, all_success = sts.read_multi_positions(SERVO_IDS)  # 读取初始位置
# Complete Taught Motions
i = 0
# while True:
#     print(f"----------第 {i+1} 次运行:----------")
#     target_pos_array = cal_target_pos(initial_pos_array)  # 补全目标位置数组
#     whether_complete = sts.multi_servos_to_target(SERVO_IDS, target_pos_array, speed=2000, acc=255)  # 同步控制到目标位置
#     whether_inplace = sts.verify_movements_to_target(SERVO_IDS, target_pos_array)
#     cmd = input("输入 'exit' 以退出，或按回车继续：")
#     if cmd.lower() == "exit":
#         print("已退出循环。")
#         break
#     print("继续运行...\n")
#     i += 1

while True:
    print(f"----------第 {i+1} 次运行:----------")

    # 1. 读取目标姿态（后面第二部分会改成“目标矩阵”）
    target_pos_array = get_target_pos()

    # 2. 构造一个 ID -> 目标位置 的字典，方便按分组取子数组
    id_to_target = dict(zip(SERVO_IDS, target_pos_array))

    # --------------- 第一步：先收四根手指 ---------------
    finger_targets = [id_to_target[sid] for sid in FINGER_SERVO_IDS]
    print(">>> 第一步：四指闭合")
    sts.multi_servos_to_target(FINGER_SERVO_IDS, finger_targets, speed=1000, acc=255)
    sts.verify_movements_to_target(FINGER_SERVO_IDS, finger_targets)

    # 可选：给一点时间缓冲
    time.sleep(3)

    # --------------- 第二步：再动大拇指 ---------------
    thumb_targets = [id_to_target[sid] for sid in THUMB_SERVO_IDS]
    print(">>> 第二步：大拇指闭合")
    sts.multi_servos_to_target(THUMB_SERVO_IDS, thumb_targets, speed=1000, acc=255)
    sts.verify_movements_to_target(THUMB_SERVO_IDS, thumb_targets)

    cmd = input("按enter回原位置:")
    if cmd == "":
        sts.multi_servos_to_target(SERVO_IDS, INITIAL_POS_ARRAY, speed=1000, acc=255)
    

    # 交互退出
    cmd = input("输入 'exit' 以退出，或按回车继续：")
    if cmd.lower() == "exit":
        print("已退出循环。")
        break
    print("继续运行...\n")
    i += 1