from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="rover_odometry",
            executable="odometry_publisher",
            name="odometry_publisher"
        ),
        Node(
            package="rover_odometry",
            executable="odometry_subscriber",
            name="odometry_subscriber"
        ),
    ])
