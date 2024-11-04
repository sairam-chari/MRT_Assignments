import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/sai/MRT_Assignments/2/ros2_ws/install/walle'
