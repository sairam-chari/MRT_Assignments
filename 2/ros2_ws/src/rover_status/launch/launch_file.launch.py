
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='',
            executable='main',
            name='main',
            output='screen',
        ),
    ])
